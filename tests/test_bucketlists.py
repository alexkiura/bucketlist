"""This module tests CRUD operations on a user's bucketlists."""
import json
from test_api import ApiTestCase


class TestBucketLists(ApiTestCase):
    """Test bucketlist actions."""

    def get_header(self):
        """
        Authenticate a user.

        Returns:
            request header with token
        """
        user = {'username': 'alex', 'password': 'foobar'}
        resp_login = self.app.post('/api/v1.0/auth/login/', data=user)
        result = json.loads(resp_login.data)
        token = result.get('Authorization').encode('ascii')
        return {'Authorization': token}

    def test_post_bucketlist(self):
        """Test creating a new bucketlist."""
        data = {'list_name': 'Travelling'}
        resp_bucketlist = self.app.post('/api/v1.0/bucketlists/',
                                        data=data, headers=self.get_header())
        result_bucketlist = json.loads(resp_bucketlist.data)
        self.assertEqual(resp_bucketlist.status_code, 200)
        self.assertEqual(result_bucketlist,
                         {'list_name': data.get('list_name'),
                          'message': 'success'})

    def test_necessary_fields(self):
        """Test mandatory fields."""
        resp_bucketlist = self.app.post('/api/v1.0/bucketlists/',
                                        headers=self.get_header())
        self.assert400(resp_bucketlist)

    def test_get_bucketlists(self):
        """Test retrieveing bucketlists."""
        self.app.post('/api/v1.0/bucketlists/', data={'list_name': 'Drinks'},
                      headers=self.get_header())
        resp_bucketlist = self.app.get('/api/v1.0/bucketlists/',
                                       headers=self.get_header())
        self.assertEqual(resp_bucketlist.status_code, 200)
        result = json.loads(resp_bucketlist.data)['bucketlists'][0]
        print result
        self.assertEqual(result.get('list_name'), 'Drinks')

    def test_put_bucketlist(self):
        """Test updating a bucketlist."""
        self.app.post('/api/v1.0/bucketlists/', data={'list_name': 'Drinks'},
                      headers=self.get_header())
        resp_bucketlist = self.app.put('/api/v1.0/bucketlists/1/',
                                       data={'list_name': 'Drinks I want'},
                                       headers=self.get_header())
        self.assertEqual(resp_bucketlist.status_code, 200)

    def test_delete_bucketlist(self):
        """Test deleting a bucketlist."""
        self.app.post('/api/v1.0/bucketlists/', data={'list_name': 'Drinks'},
                      headers=self.get_header())
        resp_bucketlist = self.app.delete('/api/v1.0/bucketlists/1/',
                                          headers=self.get_header())
        self.assertEqual(resp_bucketlist.status_code, 200)

    def test_bucketlist_pagination(self):
        """Test pagination."""
        with open('tests/list_names.in', 'r') as f:
            for list_name in f.readlines():
                self.app.post('/api/v1.0/bucketlists/',
                              data={'list_name': list_name},
                              headers=self.get_header())
        resp_bucketlist = self.app.get('/api/v1.0/bucketlists/?limit=5',
                                       headers=self.get_header())
        results = json.loads(resp_bucketlist.data)['bucketlists']
        print results
        self.assertEqual(len(results), 5)

    def test_bucketlist_search(self):
        """Test search bucketlists by name."""
        with open('tests/list_names.in', 'r') as f:
            for list_name in f.readlines():
                self.app.post('/api/v1.0/bucketlists/',
                              data={'list_name': list_name},
                              headers=self.get_header())
        resp_bucketlist = self.app.get('/api/v1.0/bucketlists/?q=Foods\n',
                                       headers=self.get_header())
        results = json.loads(resp_bucketlist.data)['bucketlists']
        self.assertEqual(len(results), 1)

    def test_single_bucketlist(self):
        """Test retrieving bucketlist by id."""
        data = {'list_name': 'Travelling'}
        self.app.post('/api/v1.0/bucketlists/',
                      data=data, headers=self.get_header())
        resp_bucketlist = self.app.get('/api/v1.0/bucketlists/1/',
                                       headers=self.get_header())
        self.assert200(resp_bucketlist)

    def test_no_bucketlist(self):
        """Test retrieving none existent bucketlists."""
        data = {'list_name': 'Travelling'}
        self.app.post('/api/v1.0/bucketlists/',
                      data=data, headers=self.get_header())
        resp_bucketlist = self.app.get('/api/v1.0/bucketlists/100/',
                                       headers=self.get_header())
        self.assertEqual(json.loads(resp_bucketlist.data),
                         {'message': 'the bucketlist was not found.'})
