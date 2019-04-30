from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps


app = Flask(__name__)
api = Api(app)


class Tracks(Resource):
    def get(self):
        return "trakcs"

class Employees_Name(Resource):
    def get(self, id):
        return id

api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<id>') # Route_3


if __name__ == '__main__':
     app.run(port='5002',host='0.0.0.0')
