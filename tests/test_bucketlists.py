"""This module tests CRUD operations on a user's bucketlists."""
import json
from test_api import ApiTestCase, db
import nose


class TestBucketLists(ApiTestCase):

    def get_header(self):
        user = {'username': 'alex', 'password': 'foobar'}
        resp_login = self.app.post('/api/v1.0/auth/login/', data=user)
        result = json.loads(resp_login.data)
        token = result.get('token').encode('ascii')
        return {'token': token}

    def test_post_bucketlist(self):
        data = {'list_name': 'Travelling'}
        resp_bucketlist = self.app.post('/api/v1.0/bucketlists/',
                                        data=data, headers=self.get_header())
        result_bucketlist = json.loads(resp_bucketlist.data)
        self.assertEqual(resp_bucketlist.status_code, 200)
        self.assertEqual(result_bucketlist,
                         {'list_name': data.get('list_name'),
                          'message': 'success'})

    def test_necessary_fields(self):
        resp_bucketlist = self.app.post('/api/v1.0/bucketlists/',
                                        headers=self.get_header())
        result_bucketlist = json.loads(resp_bucketlist.data)
        self.assertEqual(resp_bucketlist.status_code, 400)

    def test_get_bucketlists(self):
        pass
