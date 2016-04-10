"""This module contains the resources to be served on the endpoints."""
from . import api
from flask.ext.restful import Resource

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
