from datetime import datetime
from psycopg2 import sql
from query_builder.query_builder import QueryBuilder
from common.helper import parse_path


class QueryBuilderCount(QueryBuilder):
    def build(self, params):

        where = []
        values = {}

        polygon = parse_path(params.get('path', None))

        where.append("ST_Contains(ST_MakePolygon(ST_GeomFromText(%(polygon)s, 4326)), position)")
        values['polygon'] = polygon

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
        elif start_date and end_date is None:
            where.append('{date} > %(start_date)s')
            values['start_date'] = start_date
        elif end_date and start_date is None:
            where.append('{date} < %(end_date)s')
            values['end_date'] = end_date

        query = 'SELECT COUNT(*) FROM data'
        query = '{} WHERE {}'.format(query, ' AND '.join(where))
        query = format_query(query)

        return query, values


def format_query(query):
    return sql.SQL(query).format(date=sql.Identifier('date'), param_id=sql.Identifier('param_id'),
                                 mars_class=sql.Identifier('mars_class'),
                                 mars_type=sql.Identifier('mars_type'),
                                 start_date=sql.Identifier('start_date'), end_date=sql.Identifier('end_date'))
