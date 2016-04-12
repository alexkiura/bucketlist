"""This module contains the resources to be served on the endpoints."""
from flask.ext.restful import Resource, marshal
from app.models import BucketList, User
from serializers import bucketlist_serializer
from flask import g, jsonify, request
from flask.ext.httpauth import HTTPBasicAuth
from flask_restful import reqparse
from app import db

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        # try to authenticate    with username/password
        user = User.query.filter_by(username=token).first()
        if not user or not user.verify(password):
            return False
    g.user = user
    return True

class TestResource(Resource):
    def get(self):
        return {'Message': 'Welcome to my api'}


class BucketListsApi(Resource):
    @auth.login_required
    def get(self):
        bucketlists = BucketList.query.filter_by(created_by=g.user.id).all()
        return {'bucketlists': marshal(bucketlists,
                                       bucketlist_serializer)}

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('list_name')
        args = parser.parse_args()
        list_name = args['list_name']
        if list_name:
            bucketlist = BucketList(list_name=list_name, created_by=g.user.id,
                                    user_id=g.user.id)
            db.session.add(bucketlist)
            db.session.commit()
            return jsonify({'message': 'success',
                            'list_name': bucketlist.list_name})
        else:
            return jsonify({'message': 'Failure. Please provide a name for the'
                            'bucketlist'})

class BucketListApi(Resource):
    @auth.login_required
    def get(self, id):
        bucketlist = BucketList.query.filter_by(created_by=g.user.id,
                                                id=id).first()
        return {'bucketlist': marshal(bucketlist, bucketlist_serializer)}

    @auth.login_required
    def put(self, id):
        bucketlist = BucketList.query.filter_by(created_by=g.user.id,
                                                id=id).first()
        parser = reqparse.RequestParser()
        parser.add_argument('list_name')
        args = parser.parse_args()
        new_list_name = args['list_name']
        if new_list_name:
            bucketlist.list_name = new_list_name
            db.session.add(bucketlist)
            db.session.commit()
            return jsonify({'message': 'success',
                            'list_name': bucketlist.list_name})
        else:
            return jsonify({'message': 'Failure. Please provide a name for the'
                            'bucketlist'})



class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        if username and password:
            user = User.query.filter_by(username=username).first()
        else:
            return jsonify({'message':
                            'Please provide a username and password'})
        if user:
            token = user.generate_auth_token()
            return jsonify({'token': token.decode('ascii'),
                            'duration': 10000})
        else:
            return jsonify({'message':
                            'The username or password was invalid.'
                            'Please try again'})


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        if username and password:
            user = User(username=username, password=password)
        else:
            return jsonify({'message':
                            'Please provide a username and password'})
        if user:
            db.session.add(user)
            db.session.commit()
            token = user.generate_auth_token()
            return jsonify({'username': user.username,
                            'token': token.decode('ascii'),
                            'duration': 10000})
        else:
            return jsonify({'message':
                            'The registration was not successful.'
                            'Please try again'})
