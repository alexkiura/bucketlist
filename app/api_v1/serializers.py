"""This module defines the format used by marshall to map the models."""
from flask_restful import fields

bucketlistitem_serializer = {
    'item_id': fields.Integer,
    'item_name': fields.String,
    'priority': fields.String,
    'done': fields.Boolean,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}

bucketlist_serializer = {
    'id': fields.Integer,
    'list_name': fields.String,
    'bucketlist_items': fields.Nested(bucketlistitem_serializer),
    'created_by': fields.Integer,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}

user_serializer = {
    'id': fields.Integer,
    'username': fields.String,
    'bucketlists': fields.Nested(bucketlist_serializer)
}
