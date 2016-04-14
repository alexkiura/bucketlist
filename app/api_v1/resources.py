"""This module contains the resources to be served on the endpoints."""
from flask.ext.restful import Resource, marshal
from app.models import BucketList, User, BucketListItem
from serializers import bucketlist_serializer, bucketlistitem_serializer
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
        args = request.args.to_dict()
        limit, page = 10, 1
        if args:
            if args.get('limit'):
                limit = int(args.get('limit'))
            if args.get('page'):
                limit = int(args.get('page'))
            name = args.get('q')
            if name:
                search_results = BucketList.query.\
                    filter_by(created_by=g.user.id, list_name=name).\
                    paginate(page, limit, False).items
                if search_results:
                    return jsonify({'bucketlists':
                                    marshal(search_results,
                                            bucketlist_serializer)})
                else:
                    return jsonify({'message':
                                    'Bucketlist ' + name + ' doesn\'t exist.'})
        if args.keys().__contains__('q'):
            return jsonify({'message': 'Please provide a search parameter'})

        if limit and page:
            print 'limit is', limit, 'page is', page
            bucketlists = BucketList.query.\
                filter_by(created_by=g.user.id).paginate(
                    page, limit, False).items
        else:
            bucketlists = BucketList.query.filter_by(
                created_by=g.user.id).all()
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
        if bucketlist:
            return {'bucketlist': marshal(bucketlist, bucketlist_serializer)}
        else:
            return jsonify({'message': 'the bucketlist was not found.'})

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

    @auth.login_required
    def delete(self, id):
        bucketlist = BucketList.query.filter_by(created_by=g.user.id,
                                                id=id).first()
        if bucketlist:
            db.session.delete(bucketlist)
            db.session.commit()
            return jsonify({'message': 'successfully deleted bucketlist'})
        else:
            return jsonify({'message': 'the delete was unsuccessful.'})



class BucketListItemsApi(Resource):

    @auth.login_required
    def get(self, id):
        args = request.args.to_dict()
        if args:
            limit = int(args.get('limit'))
            page = int(args.get('page'))
            if limit and page:
                bucketlistitems = BucketListItem.query.filter_by(bucketlist_id=id).\
                 paginate(page, limit, False).items
        else:
            bucketlistitems = BucketListItem.query.filter_by(bucketlist_id=id).\
              all()
        return jsonify({'items':
                       marshal(bucketlistitems, bucketlistitem_serializer)})

    @auth.login_required
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('item_name')
        parser.add_argument('priority')
        args = parser.parse_args()
        item_name = args['item_name']
        priority = args['priority']
        done = False

        if item_name and priority:
            bucketlistitem = BucketListItem(item_name=item_name,
                                            priority=priority,
                                            done=done,
                                            bucketlist_id=id)
            db.session.add(bucketlistitem)
            db.session.commit()
            return jsonify({'message': 'successfully created item.',
                            'item_name': bucketlistitem.item_name})


class BucketListItemApi(Resource):

    @auth.login_required
    def get(self, id, item_id):
        bucketlistitem = BucketListItem. \
            query.filter_by(bucketlist_id=id, item_id=item_id).first()
        return jsonify({'item':
                       marshal(bucketlistitem, bucketlistitem_serializer)})

    @auth.login_required
    def put(self, id, item_id):
        bucketlistitem = BucketListItem. \
            query.filter_by(bucketlist_id=id, item_id=item_id).first()
        parser = reqparse.RequestParser()
        parser.add_argument('item_name')
        parser.add_argument('priority')
        parser.add_argument('done')
        args = parser.parse_args()
        item_name = args['item_name']
        priority = args['priority']
        done = args['done']
        if item_name or priority or done:
            bucketlistitem.item_name = item_name
            bucketlistitem.priority = priority
            bucketlistitem.done = done
        db.session.add(bucketlistitem)
        db.session.commit()
        return jsonify({'message': 'successfully updated item.',
                        'item_name': bucketlistitem.item_name})

    @auth.login_required
    def delete(self, id, item_id):
        bucketlistitem = BucketListItem. \
            query.filter_by(bucketlist_id=id, item_id=item_id).first()
        if bucketlistitem:
            db.session.delete(bucketlistitem)
            db.session.commit()
            return jsonify({'message':
                            'successfully deleted bucketlistitem'})
        else:
            return jsonify({'message': 'the delete was unsuccessful.'})


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
