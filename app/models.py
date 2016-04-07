"""Models for bucketlist API V1."""
from app.database import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    """Defines the user table and operations allowed."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(128))

    @property
    def username(self):
        return self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @property.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username




class BucketItem:
    """."""

    pass
