"""This module contains the resources to be served on the endpoints."""
from flask.ext.restful import Resource

class TestResource(Resource):
    def get(self):
        return {'Message': 'Welcome to my api'}
