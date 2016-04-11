"""This module configures and creates a Flask app instance."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
from config.config import config
# import ipdb; ipdb.set_trace()

db = SQLAlchemy()


def create_app(config_name):
    """
    Create a Flask application instance.

    Args:
        config_name (str): A configuration to use for the application.

    Returns:
        app: A Flask application instance with necessary
        extensions initialized and bluePrints registered.
    """
    app = Flask(__name__)
    # app.config.from_object(config[config_name])
    app.config.from_object(config[config_name])
    db.init_app(app)
    # import ipdb; ipdb.set_trace()
    # from .api_v1 import api_v1 as api_1_blueprint
    # app.register_blueprint(api_1_blueprint, url_prefix='/api/v1.0')
    # app.register_blueprint(api_1_blueprint)

    return app

flask_app = create_app('development')
# api = Api(flask_app)
