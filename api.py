from flask import Flask
from flask_restful import Api
from model.search_circle import SearchCircle
from model.search_polygon import SearchPolygon
import csv

app = Flask(__name__)
api = Api(app)

api.add_resource(SearchCircle,
                 '/search/<float:lat>,<float:lon>/<int:radius>/')

api.add_resource(SearchPolygon,
                 '/search/<float:latmin>-<float:lonmin>,<float:latmax>-<float:lonmax>/')

if __name__ == '__main__':
    app.run(debug=True)
