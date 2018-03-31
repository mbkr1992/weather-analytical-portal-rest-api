from response_builder.response_builder import ResponseBuilder
from geojson import Feature, FeatureCollection, Point


class GeoJsonBuilder(ResponseBuilder):
    def build(self, result):
        return FeatureCollection([to_feature(r) for r in result])


def to_feature(param):
    geojson_point, date, name, value = param
    latitude, longitude = geojson_point.coords
    position = Point(longitude, latitude)
    return Feature(geometry=position, properties=dict(
        date=date.isoformat(),
        name=name,
        value=value
    ))
