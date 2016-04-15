"""This module tests user creation and log in."""
import json
from test_api import ApiTestCase
from app.models import User


class TestUserAuth(ApiTestCase):
    """Test user authentication and registration."""

    def test_user_register(self):
        """Test user registration."""
        self.user = {'username': 'makmende', 'password': 'foobar'}
        result = self.app.post('/api/v1.0/auth/register/', data=self.user)
        self.assertEqual(result.status_code, 200)
        resp_data = json.loads(result.data)
        self.assertTrue('token' in resp_data)
        self.assertTrue('username' in resp_data)
        self.assertEqual(resp_data.get('username'), self.user['username'])

    def test_user_login(self):
        """Test user login."""
        self.user = {'username': 'alex', 'password': 'foobar'}
        result = self.app.post('/api/v1.0/auth/login/', data=self.user)
        resp_data = json.loads(result.data)
        self.assertTrue('token' in resp_data)
        self.assertTrue('duration' in resp_data)

    def test_incorrect_login(self):
        """Test incorrect credentials."""
        self.user = {'username': 'alex', 'password': '123'}
        result = self.app.post('/api/v1.0/auth/login/', data=self.user)
        resp_data = json.loads(result.data)
        self.assertEqual(resp_data, {'message':
                                     'The username or password was invalid.'
                                     'Please try again'})

    def test_unallowed_fields(self):
        """Test getting unauthorised fields."""
        user = User(username='james', password='007')
        with self.assertRaises(AttributeError):
            user.password
