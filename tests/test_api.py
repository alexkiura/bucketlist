"""This module Initializes the API test case."""

from flask_testing import TestCase
from server import app, db
from app.models import User
from config.config import config
import json
import nose


class ApiTestCase(TestCase):
    """Test API creation."""

    def create_app(self, app=app):
        """Create a flask instance."""
        app.config.from_object(config['testing'])
        return app

    def setUp(self):
        """Setup testcase."""
        self.app = self.create_app().test_client()
        db.create_all()
        # create & add test user
        alex = User(username='alex', password='foobar')
        db.session.add(alex)
        db.session.commit()

    def test_index_route(self):
        """Test /api/v1.0/."""
        result = self.app.get('/api/v1.0/')
        result = json.loads(result.data)
        self.assertEqual(result, {'Message': 'Welcome to my api'})

    def tearDown(self):
        """Clean up."""
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    nose.run()
