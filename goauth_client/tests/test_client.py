from __future__ import print_function

from goauth_client import client
import unittest
from bs4 import BeautifulSoup



class GOAuthClientHelloTest(unittest.TestCase):

    def setUp(self):
        client.app.config['TESTING'] = True
        self.app = client.app.test_client()

    def tearDown(self):
        pass

    def test_page_titles(self):
        # Check the base template title string
        rv = self.app.get('/')
        soup = BeautifulSoup(rv.data, 'html.parser')
        assert soup.title.string.endswith(' - Globus Auth Client Example')

        # Check that each individual page has it's respective title.
        assert soup.title.string.startswith('Home')


if __name__ == '__main__':
    unittest.main()
