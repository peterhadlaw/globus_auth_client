from goauth_client import client
import unittest


class GOAuthClientHelloTest(unittest.TestCase):

    def setUp(self):
        client.app.config['TESTING'] = True
        self.app = client.app.test_client()

    def tearDown(self):
        pass

    def test_home_heading(self):
        rv = self.app.get('/')
        pass

if __name__ == '__main__':
    unittest.main()
