"""This module contains various configuration options."""


class Config:
    """Base configuration."""

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
    DATABASE_URI = 'sqlite:///dbucketlist.db'


class TestConfig(Config):
    """Testing configuration."""

    TESTING = True
    DATABASE_URI = 'sqlite:///tbucketlist.db'


class ProductionConfig(Config):
    """Production configurations."""

    DEBUG = False
    DATABASE_URI = 'sqlite:///bucketlist.db'

config = {
    'development': DevConfig,
    'testing': TestConfig,
    'Production': ProductionConfig
}
