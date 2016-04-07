import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite:///bucketlist.db'
