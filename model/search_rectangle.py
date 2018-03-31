from flask import request
from flask_restful import Resource

from db.db_handler import perform_select
from query_builder.query_builder_factory import QueryBuilderFactory
from response_builder.response_factory import ResponseFactory


class SearchRectangle(Resource):
    def get(self, latmin, latmax, lonmin, lonmax):
        date = request.args.get('date')
        param_id = request.args.get("param_id")
        mars_class = request.args.get("mars_class")
        mars_type = request.args.get("mars_type")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        limit = request.args.get("limit")
        page = request.args.get("page")

        query, value = QueryBuilderFactory.get_type('rectangle').build({
            latmin: latmin,
            lonmin: lonmin,
            latmax: latmax,
            lonmax: lonmax,
            date: date,
            param_id: param_id,
            mars_class: mars_class,
            mars_type: mars_type,
            start_date: start_date,
            end_date: end_date,
            limit: limit,
            page: page,
        })

        result = perform_select(query, value)

        response_type = request.args.get("response_type")
        response_builder = ResponseFactory.get_type(response_type)
        response = response_builder.build(result)

        return response
