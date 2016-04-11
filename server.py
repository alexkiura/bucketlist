"""This module runs the api server."""
import os
from app import flask_app, db
from app.models import User, BucketList, BucketListItem
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.restful import Resource, Api
from app.api_v1.resources import TestResource, \
    BucketListApi, UserLogin, UserRegister

app = flask_app
api = Api(app=app, prefix='/api/v1.0')
manager = Manager(app)
migrate = Migrate(app, db)

# add resources
api.add_resource(TestResource, '/')
api.add_resource(BucketListApi, '/bucketlists/')
api.add_resource(UserLogin, '/auth/login/')
api.add_resource(UserRegister, '/auth/register/')


def make_shell_context():
    """Add app, database and models to the shell."""
    return dict(app=app, db=db, User=User, BucketList=BucketList,
                BucketListItem=BucketListItem)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def run_tests():
    """Run tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
