from flask_restful import Resource
from flask import request
from geojson import Feature, FeatureCollection, Point
from psycopg2 import connect, extras, sql
from postgis.psycopg import register
from datetime import datetime
from math import ceil, floor
DBN = 'dbname=portal user=postgres'


class Reading(Resource):
    pass


class Readings(Resource):
    def get(self):
        query, data = construct_query()
        items = sample_select(query, data)

        if items:
            features = FeatureCollection([to_feature(item) for item in items])
            return features


def construct_query():
    where = []
    values = {}

    # query_station = 'Select s.position, sd.date, sd.name, sd.value from station_data as sd INNER JOIN station as s ON sd.station_id = s.id'
    query = 'Select sd.position, sd.date, sd.name, sd.value from data as sd'

    date_param = request.args.get('date')
    if date_param:
        date = datetime.strptime(date_param, '%Y-%m-%dT%H:%M:%S')
        where.append('{date} = %(date)s')
        values['date'] = date

    param_id = request.args.get("param_id")
    if param_id:
        where.append('{param_id} = %(param_id)s')
        values['param_id'] = param_id

    mars_class = request.args.get("mars_class")
    if mars_class:
        where.append('{mars_class} = %(mars_class)s')
        values['mars_class'] = mars_class

    mars_type = request.args.get("mars_type")
    if mars_type:
        where.append('{mars_type} = %(mars_type)s')
        values['mars_type'] = mars_type

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if start_date and end_date:
        where.append('{date} BETWEEN %(start_date)s AND %(end_date)s')
        values['start_date'] = start_date
        values['end_date'] = end_date

    limit = request.args.get("limit") or 50
    page = request.args.get("page") or 0

    offset = int(page) * int(limit)
    query_part_limit = 'LIMIT {} OFFSET {}'.format(limit, offset)

    if where:
        # query_station = '{} WHERE {} {}'.format(query_station, ' AND '.join(where), query_part_limit)
        query = '{} WHERE {} {}'.format(query, ' AND '.join(where), query_part_limit)
        # query = '({}) UNION ({})'.format(query_station, query_satellite)
    else:
        # query_station = '{} {}'.format(query_station, query_part_limit)
        query = '{} {}'.format(query, query_part_limit)
        # query = '({}) UNION ({})'.format(query_station, query_satellite)

    query = sql.SQL(query).format(date=sql.Identifier('date'), param_id=sql.Identifier('param_id'),
                                  mars_class=sql.Identifier('mars_class'), mars_type=sql.Identifier('mars_type'),
                                  start_date=sql.Identifier('start_date'), end_date=sql.Identifier('end_date'))
    return query, values


def to_feature(item):
    position = Point(item["position"].coords)
    feature = Feature(geometry=position, properties={
        "date": item["date"].isoformat(),
        "name": item["name"],
        "value": item["value"],
    })
    return feature


def sample_select(query, data):
    with connect(DBN) as conn:
        register(connection=conn)
        with conn.cursor(cursor_factory=extras.DictCursor) as curs:
            curs.execute(query, data)
            return curs.fetchall()
