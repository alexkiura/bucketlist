"""This module tests CRUD operations on a bucketlists' bucketitems."""
import json
from test_api import ApiTestCase


class TestBucketListItems(ApiTestCase):
    """Test bucketlist items actions."""

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

    def add_bucketlist(self):
        """Create new bucketlist to test bucketlist item actions."""
        data = {'list_name': 'Travelling'}
        resp_bucketlist = self.app.post('/api/v1.0/bucketlists/',
                                        data=data, headers=self.get_header())
        if resp_bucketlist.status_code == 200:
            return True
        return False

    def test_post_bucketlistitem(self):
        """Test adding an item to a bucketlist."""
        self.add_bucketlist()
        data = {'item_name': 'travel to Canada', 'priority': 'High'}
        resp = self.app.post('/api/v1.0/bucketlists/1/items/', data=data,
                             headers=self.get_header())
        self.assertIn(data['item_name'], resp.data)
        self.assertEqual(resp.status_code, 201)

    def test_get_bucketlistitems(self):
        """Test retrieveing all bucketlist items."""
        self.add_bucketlist()
        data = {'item_name': 'travel to Canada', 'priority': 'High'}
        self.app.post('/api/v1.0/bucketlists/1/items/', data=data,
                      headers=self.get_header())
        resp = self.app.get('/api/v1.0/bucketlists/1/items/',
                            headers=self.get_header())
        self.assert200(resp)

    def test_put_bucketlistitem(self):
        """Test updating bucketlist items."""
        self.add_bucketlist()
        data = {'item_name': 'travel to Columbia', 'priority': 'Medium'}
        self.app.post('/api/v1.0/bucketlists/1/items/', data=data,
                      headers=self.get_header())
        data['item_name'] = 'Travel to Liberia'
        data['done'] = False
        resp = self.app.put('/api/v1.0/bucketlists/1/items/1/',
                            data=data,
                            headers=self.get_header())
        self.assert200(resp)
        self.assertEqual(json.loads(resp.data),
                         {'item_name': data['item_name'],
                          'Message': 'Successfully updated item.'})

    def test_delete_bucketlistitem(self):
        """Test deleting a bucketlist item."""
        self.add_bucketlist()
        data = {'item_name': 'travel to Columbia', 'priority': 'Medium'}
        self.app.post('/api/v1.0/bucketlists/1/items/', data=data,
                      headers=self.get_header())
        resp = self.app.delete('/api/v1.0/bucketlists/1/items/1/',
                               headers=self.get_header())
        self.assert200(resp)

    def test_bucketlistitem_pagination(self):
        """Test pagination and limiting results."""
        self.add_bucketlist()
        with open('tests/item_names.in', 'r') as f:
            for item_name in f.readlines():
                self.app.post('/api/v1.0/bucketlists/1/items/',
                              data={'item_name': item_name,
                                    'priority': 'High'},
                              headers=self.get_header())
        resp = self.app.get('/api/v1.0/bucketlists/1/items/?limit=4&page=1',
                            headers=self.get_header())
        results = json.loads(resp.data)
        self.assertEqual(len(results), 4)
