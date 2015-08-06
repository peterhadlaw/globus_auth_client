from __future__ import print_function

from goauth_client import client
import unittest
from bs4 import BeautifulSoup



class GOAuthClientAuthTest(unittest.TestCase):

    def setUp(self):
        client.app.config['TESTING'] = True
        self.app = client.app.test_client()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
