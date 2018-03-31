from flask import request
from flask_restful import Resource

from db.db_handler import perform_select_count
from query_builder.query_builder_factory import QueryBuilderFactory


class SearchPolygonCount(Resource):
    def get(self):
        path = request.args.get('path')
        date = request.args.get('date')
        param_id = request.args.get("param_id")
        mars_class = request.args.get("mars_class")
        mars_type = request.args.get("mars_type")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        query, value = QueryBuilderFactory.get_type('polygon-count').build(dict(
            path=path,
            date=date,
            param_id=param_id,
            mars_class=mars_class,
            mars_type=mars_type,
            start_date=start_date,
            end_date=end_date,
        ))

        result = perform_select_count(query, value)
        return result
