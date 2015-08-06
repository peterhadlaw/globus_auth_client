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

    def test_page_headings(self):
        rv = self.app.get('/')
        soup = BeautifulSoup(rv.data, 'html.parser')
        assert soup.h1.string == "Globus Auth Demo of XSEDE Client App"

    def test_page_has_contents(self):
        rv = self.app.get('/')
        soup = BeautifulSoup(rv.data, 'html.parser')
        assert soup.find(id="page-content").text != ''

if __name__ == '__main__':
    unittest.main()
