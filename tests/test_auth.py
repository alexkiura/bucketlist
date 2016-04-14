"""This module tests user creation and log in."""
import json
from test_api import ApiTestCase, db
import nose

class TestUserAuth(ApiTestCase):

    def test_user_register(self):
        self.user = {'username': 'makmende', 'password': 'foobar'}
        result = self.app.post('/api/v1.0/auth/register/', data=self.user)
        self.assertEqual(result.status_code, 200)
        resp_data = json.loads(result.data)
        self.assertTrue(resp_data.has_key('token'))
        self.assertTrue(resp_data.has_key('username'))
        self.assertEqual(resp_data.get('username'), self.user['username'])

    def test_user_login(self):
        self.user = {'username': 'alex', 'password': 'foobar'}
        result = self.app.post('/api/v1.0/auth/login/', data=self.user)
        resp_data = json.loads(result.data)
        print resp_data
        self.assertTrue(resp_data.has_key('token'))
        self.assertTrue(resp_data.has_key('duration'))
