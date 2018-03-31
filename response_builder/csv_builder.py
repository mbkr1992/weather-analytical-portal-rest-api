from response_builder.response_builder import ResponseBuilder
from flask import make_response
import csv


class CSVBuilder(ResponseBuilder):
    def build(self, result):
        response = [to_dict(r) for r in result]
        with open('temp/export.csv', 'w+') as file:
            csv_writer = csv.writer(file)
            for index, item in enumerate(response):
                if index == 0:
                    csv_writer.writerow(item.keys())
                csv_writer.writerow(item.values())

        with open('temp/export.csv', 'r') as file:
            output = make_response(file.read())
            output.headers["Content-Disposition"] = "attachment; filename=export.csv"
            output.headers["Content-type"] = "text/csv"
        return output


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
