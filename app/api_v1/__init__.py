"""This module creates the api BluePrint."""

from flask import Blueprint
from flask.ext.restful import Api
from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from app import create_app

app = create_app()
api = Api(app)
api_1_blueprint = Blueprint('api_1_blueprint', __name__)
