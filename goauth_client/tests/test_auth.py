from __future__ import print_function

from goauth_client import client
import unittest
from bs4 import BeautifulSoup
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import quote as urlquote


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

    def test_auth_oauth_no_auth_provided(self):
        # If no auth code or error provided, check for Login Required notice
        rv = self.app.get('/profile')
        soup = BeautifulSoup(rv.data, 'html.parser')
        assert soup.h1.string == "Login Required"

    def test_auth_oauth_error(self):
        # If there was an error from the oauth flow, display it
        err = "Sample Error"
        err_desc = "Sample Error Description"

        # Just the error, no description
        rv = self.app.get('/profile?error={}'.format(urlquote(err)))
        soup = BeautifulSoup(rv.data, 'html.parser')
        assert soup.find(id="login-error").string.strip() == err

        # Both error and error description
        rv = self.app.get('/profile?error={}&error_description={}'
                          .format(urlquote(err), urlquote(err_desc)))
        soup = BeautifulSoup(rv.data, 'html.parser')
        assert soup.find(id="login-error").string.strip() == err
        assert soup.find(id="login-error-description").string.strip() == err_desc

if __name__ == '__main__':
    unittest.main()
