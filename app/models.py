"""Models for bucketlist API V1."""
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from config.config import config

class BucketListItem(db.Model):
    """Defines the items in a user's bucketlist."""

    __tablename__ = "bucketlistitems"
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(256), unique=True)
    priority = db.Column(db.String(50))
    done = db.Column(db.Boolean(), default=False, index=True)
    date_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        """Return a string representation of the user."""
        return '<BucketListItem %r>' % self.item_name


class BucketList(db.Model):
    """Defines a user's BucketList and operations allowed."""

    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(100), unique=True)
    bucketlist_items = db.relationship('BucketListItem', backref='bucketlist')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer)

    def __repr__(self):
        """Return a string representation of the bucketlist."""
        return '<BucketList %r>' % self.list_name


class User(db.Model):
    """
    This represents the user model.

    Attributes:
        id (int): A user's id.
        username (str): A unique identifier for a user.
        bucketlists (relationship): A user's bucketlists.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    bucketlists = db.relationship('BucketList', backref='user')

    def verify(self, password):
        """
        Verify a user's password.

        Args:
            password

        Returns:
            bool: True if the hash value of password mathes a user's
            stored password hash.
        """
        return check_password_hash(self.password_hash, str(password))

    def __init__(self, **kwargs):
        """Initialize a user object."""
        self.username = kwargs['username']
        self.password_hash = generate_password_hash(str(kwargs['password']))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Generate and save a hash of <password>."""
        self.password_hash = generate_password_hash(password)

    def generate_auth_token(self, expiration=10000):
        token_serializer = Serializer(config['SECRET_KEY'],
                                      expires_in=expiration)
        return token_serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        token_serializer = Serializer(config['SECRET_KEY'])
        try:
            data = token_serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        """Return a string representation of the user."""
        return '<User %r>' % self.username
