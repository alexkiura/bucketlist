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
    """
    Verify a user's password.

    Args:
        token:
        password:
    retuns:
        True if the password is correct.
    """
    token = request.headers.get('Authorization')
    if token is not None:
        user = User.verify_auth_token(token)
        if user:
            g.user = user
            return True
    return False


class IndexResource(Resource):
    """
    Manage responses to the index route.

    URL:
        /api/v1.0/
    Methods:
        GET
    """

    def get(self):
        """Return a welcome message."""
        return {'Message': 'Welcome to my api'}


class BucketListsApi(Resource):
    """
    Manage responses to bucketlists requests.

    URL:
        /api/v1.0/bucketlists/

    Methods:
        GET, POST
    """

    @auth.login_required
    def get(self):
        """
        Retrieve created bucketlists.

        Returns:
            json: A list of bucketlists created by the user.
        """
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
        """
        Create a new bucketlist.

        Returns:
            A resonse indicating success.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('list_name', required=True,
                            help='list_name can not be blank')
        args = parser.parse_args()
        list_name = args['list_name']
        if list_name:
            bucketlist = BucketList(list_name=list_name, created_by=g.user.id,
                                    user_id=g.user.id)
            db.session.add(bucketlist)
            db.session.commit()
            return jsonify({'message': 'success',
                            'list_name': bucketlist.list_name})


class BucketListApi(Resource):
    """
    Manage responses to bucketlists requests.

    URL:
        /api/v1.0/bucketlists/<id>/

    Methods:
        GET, PUT, DELETE
    """

    @auth.login_required
    def get(self, id):
        """
        Retrieve the bucketlist using an id.

        Args:
            id: The id of the bucketlist to be retrieved

        Returns:
            json: The bucketlist with the id.
        """
        bucketlist = BucketList.query.filter_by(created_by=g.user.id,
                                                id=id).first()
        if bucketlist:
            return {'bucketlist': marshal(bucketlist, bucketlist_serializer)}
        else:
            return jsonify({'message': 'the bucketlist was not found.'})

    @auth.login_required
    def put(self, id):
        """
        Update a bucketlist.

        Args:
            id: The id of the bucketlist to be updated

        Returns:
            json: response with success or failure message.
        """
        bucketlist = BucketList.query.filter_by(created_by=g.user.id,
                                                id=id).first()
        parser = reqparse.RequestParser()
        parser.add_argument('list_name', required=True,
                            help='list_name can not be blank')
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
        """
        Delete a bucketlist.

        Args:
            id: The id of the bucketlist to be updated

        Returns:
            json: response with success or failure message.
        """
        bucketlist = BucketList.query.filter_by(created_by=g.user.id,
                                                id=id).first()
        if bucketlist:
            db.session.delete(bucketlist)
            db.session.commit()
            return jsonify({'message': 'successfully deleted bucketlist'})
        else:
            return jsonify({'message': 'the delete was unsuccessful.'})


class BucketListItemsApi(Resource):
    """
    Manage responses to bucketlist itemsrequests.

    URL:
        /api/v1.0/bucketlists/<id>/items/

    Methods:
        GET, POST
    """

    @auth.login_required
    def get(self, id):
        """
        Retrieve bucketlist items.

        Args:
            id: The id of the bucketlist from which to retrieve items

        Returns:
            json: response with bucketlist items.
        """
        limit, page = 10, 1
        args = request.args.to_dict()
        if args:
            if args.get('limit'):
                limit = int(args.get('limit'))
            if args.get('page'):
                page = int(args.get('page'))
            if limit and page:
                bucketlistitems = BucketListItem.\
                    query.filter_by(bucketlist_id=id).\
                    paginate(page, limit, False).items
        else:
            bucketlistitems = BucketListItem.\
                query.filter_by(bucketlist_id=id).all()
        return jsonify({'items':
                       marshal(bucketlistitems, bucketlistitem_serializer)})

    @auth.login_required
    def post(self, id):
        """
        Add anitem to a bucketlist.

        Args:
            id: The id of the bucketlist to add item

        Returns:
            json: response with success message and item name.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('item_name', required=True,
                            help='item_name can not be blank')
        parser.add_argument('priority', required=True,
                            help='priority can not be blank')
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
    """
    Manage responses to bucketlist items requests.

    URL:
        /api/v1.0/bucketlists/<id>/items/<item_id>/

    Methods:
        GET, POST
    """

    @auth.login_required
    def put(self, id, item_id):
        """
        Update a bucketlist item.

        Args:
            id: The id of the bucketlist with the item
            item_id: The id of the item being updated

        Returns:
            json: A response with a success message.
        """
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
        """
        Delete a bucketlist item.

        Args:
            id: The id of the bucketlist with the item
            item_id: The id of the item being deleted

        Returns:
            json: A response with a success/ failure message.
        """
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
    """
    Manage responses to user requests.

    URL:
        /api/v1.0/auth/login/

    Methods:
        POST
    """

    def post(self):
        """
        Authenticate a user.

        Returns:
            json: authentication token, expiration duration or error message.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help='username can not be blank')
        parser.add_argument('password', required=True,
                            help='password can not be blank')
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        if username and password:
            user = User.query.filter_by(username=username).first()
        else:
            return jsonify({'message':
                            'Please provide a username and password'})
        if user and user.verify(password):
            token = user.generate_auth_token()
            return jsonify({'Authorization': token.decode('ascii')})
        else:
            return jsonify({'message':
                            'The username or password was invalid.'
                            'Please try again'})


class UserRegister(Resource):
    """
    Manage responses to user requests.

    URL:
        /api/v1.0/auth/register/

    Methods:
        POST
    """

    def post(self):
        """
        Register a user.

        Returns:
            json: authentication token, username and duration or error message.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help='username can not be blank')
        parser.add_argument('password', required=True,
                            help='password can not be blank')
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
            return jsonify({'Authorization': token.decode('ascii')})
        else:
            return jsonify({'message':
                            'The registration was not successful.'
                            'Please try again'})
