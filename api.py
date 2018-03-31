from flask import Flask
from flask_restful import Api
from model.search_circle import SearchCircle
from model.search_rectangle import SearchRectangle
from common.float_converter import FloatConverter


app = Flask(__name__)
app.url_map.converters['float'] = FloatConverter

api = Api(app)


api.add_resource(SearchCircle,
                 '/search/<float:lat>,<float:lon>/<int:radius>')

api.add_resource(SearchRectangle,
                 '/search/<float:latmin>-<float:latmax>,<float:lonmin>-<float:lonmax>')



if __name__ == '__main__':
    app.run(debug=True)
