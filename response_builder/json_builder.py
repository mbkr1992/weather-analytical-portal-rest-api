from response_builder.response_builder import ResponseBuilder
import json


class JsonBuilder(ResponseBuilder):
    def build(self, result):
        return [to_dict(r) for r in result]


def to_dict(param):

    position, date, name, value = param
    longitude, latitude = position
    return dict(
        latitude=latitude,
        longitude=longitude,
        date=date.isoformat(),
        name=name,
        value=value,
    )
