from response_builder.response_builder import ResponseBuilder


class EmptyBuilder(ResponseBuilder):
    def build(self, items):
        pass
