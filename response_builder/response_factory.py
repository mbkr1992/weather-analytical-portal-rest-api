from response_builder.json_builder import JsonBuilder
from response_builder.geo_json_builder import GeoJsonBuilder
from response_builder.empty_builder import EmptyBuilder
from response_builder.csv_builder import CSVBuilder


class ResponseFactory:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_type(response_type):
        if response_type:
            if response_type.lower() == 'json':
                return JsonBuilder()
            elif response_type.lower() == 'geojson':
                return GeoJsonBuilder()
            elif response_type.lower() == 'csv':
                return CSVBuilder()
            else:
                return EmptyBuilder()
        else:
            return JsonBuilder()