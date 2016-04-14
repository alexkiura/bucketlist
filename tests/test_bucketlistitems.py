"""This module tests CRUD operations on a bucketlists' bucketitems."""
import json
from test_api import ApiTestCase, db
import nose


class TestBucketListItemss(ApiTestCase):

    def get_header(self):
        user = {'username': 'alex', 'password': 'foobar'}
        resp_login = self.app.post('/api/v1.0/auth/login/', data=user)
        result = json.loads(resp_login.data)
        token = result.get('token').encode('ascii')
        return {'token': token}

    def add_bucketlist(self):
        data = {'list_name': 'Travelling'}
        resp_bucketlist = self.app.post('/api/v1.0/bucketlists/',
                                        data=data, headers=self.get_header())
        if resp_bucketlist.status_code == 200:
            return True
        return False

    def test_post_bucketlistitem(self):
        self.add_bucketlist()
        data = {'item_name': 'travel to Canada', 'priority': 'High'}
        resp = self.app.post('/api/v1.0/bucketlists/1/items/', data=data,
                             headers=self.get_header())
        self.assert200(resp)
        self.assertEqual(json.loads(resp.data),
                         {'message': 'successfully created item.',
                          'item_name': data['item_name']})
