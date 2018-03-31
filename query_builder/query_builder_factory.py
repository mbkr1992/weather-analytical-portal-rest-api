from query_builder.query_builder_circle import QueryBuilderCircle
from query_builder.query_builder_empty import QueryBuilderEmpty
from query_builder.query_builder_polygon import QueryBuilderPolygon
from query_builder.query_builder_count import QueryBuilderCount
from query_builder.query_builder_rectangle import QueryBuilderRectangle


class QueryBuilderFactory:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_type(response_type):
        if response_type:
            if response_type.lower() == 'point':
                return QueryBuilderCircle()
            elif response_type.lower() == 'rectangle':
                return QueryBuilderRectangle()
            elif response_type.lower() == 'polygon':
                return QueryBuilderPolygon()
            elif response_type.lower() == 'polygon-count':
                return QueryBuilderCount()
            else:
                return QueryBuilderEmpty()
        else:
            return QueryBuilderEmpty()