from __future__ import print_function

from goauth_client import client
import unittest
from bs4 import BeautifulSoup



class GOAuthClientAuthTest(unittest.TestCase):

    def setUp(self):
        client.app.config['TESTING'] = True
        # Needed to test `url_for`
        client.app.config['SERVER_NAME'] = 'localhost'
        self.app = client.app.test_client()

    def tearDown(self):
        pass

    def test_auth_url_added_to_button(self):
        auth_url = client.establishFlow().step1_get_authorize_url()
        paths = ['/', '/profile']
        for path in paths:
            rv = self.app.get(path)
            soup = BeautifulSoup(rv.data, 'html.parser')
            assert soup.find('a', class_="btn-primary")['href'] == auth_url

if __name__ == '__main__':
    unittest.main()
