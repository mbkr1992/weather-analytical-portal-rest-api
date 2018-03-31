from datetime import datetime

from psycopg2 import sql

from query_builder.query_builder import QueryBuilder


class QueryBuilderCircle(QueryBuilder):
    def build(self, params):
        query = 'SELECT position, date, name, value FROM data'
        where = []
        values = {}

        # 13.404954﻿, 52.520008
        lat = params.get('lat', 50.7827)
        lon = params.get('lon', 6.0941)
        radius = (params.get('radius', 1) * 1000)  # 1km

        where.append('ST_DWithin(position, ST_MakePoint(%(lon)s, %(lat)s)::geography, %(radius)s)')
        values['lat'] = lat
        values['lon'] = lon
        values['radius'] = radius

        date = params.get('date', None)
        if date:
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            where.append('{date} = %(date)s')
            values['date'] = date

        param_id = params.get("param_id", None)
        if param_id:
            where.append('{param_id} = %(param_id)s')
            values['param_id'] = param_id

        mars_class = params.get("mars_class", None)
        if mars_class:
            where.append('{mars_class} = %(mars_class)s')
            values['mars_class'] = mars_class

        mars_type = params.get("mars_type", None)
        if mars_type:
            where.append('{mars_type} = %(mars_type)s')
            values['mars_type'] = mars_type

        start_date = params.get("start_date", None)
        end_date = params.get("end_date", None)
        if start_date and end_date:
            where.append('{date} BETWEEN %(start_date)s AND %(end_date)s')
            values['start_date'] = start_date
            values['end_date'] = end_date

        limit = params.get("limit", 50)
        page = params.get("page", 0)
        offset = int(page) * int(limit)

        query = '{} WHERE {} LIMIT {} OFFSET {}'.format(query, ' AND '.join(where), limit, offset)
        query = sql.SQL(query).format(date=sql.Identifier('date'), param_id=sql.Identifier('param_id'),
                                      mars_class=sql.Identifier('mars_class'),
                                      mars_type=sql.Identifier('mars_type'),
                                      start_date=sql.Identifier('start_date'), end_date=sql.Identifier('end_date'))
        return query, values
    pass