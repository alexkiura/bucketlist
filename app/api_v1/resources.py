"""This module contains the resources to be served on the endpoints."""
from flask.ext.restful import Resource, marshal
from app.models import BucketList

class TestResource(Resource):
    def get(self):
        return {'Message': 'Welcome to my api'}


class BucketListApi(Resource):
    def get(self):
        return {'bucketlists': marshal(BucketList.query.all())}
