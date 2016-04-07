"""This module configures and creates a Flask app instance."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """
    Create a Flask application instance.

    Args:
        config_name (str): A configuration to use for the application.

    Returns:
        app: A Flask application instance with necessary
        extensions initialized and bluePrints registered.
    """
    app = Flask(__name__)
    db.init_app(app)

    from .api_v1 import api as api_1_blueprint
    app.register_blueprint(api_1_blueprint, url_prefix='/api/v1.0')

    return app
