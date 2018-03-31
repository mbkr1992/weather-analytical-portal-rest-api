from query_builder.query_builder import QueryBuilder


class QueryBuilderEmpty(QueryBuilder):
    def build(self, params):
        pass