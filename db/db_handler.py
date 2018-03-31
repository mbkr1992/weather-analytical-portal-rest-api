from psycopg2 import connect, extras, sql
from postgis.psycopg import register
DBN = 'dbname=portal user=postgres'


def perform_select(query, data):
    with connect(DBN) as conn:
        register(connection=conn)
        with conn.cursor(cursor_factory=extras.DictCursor) as curs:
            curs.execute(query, data)
            return curs.fetchall()