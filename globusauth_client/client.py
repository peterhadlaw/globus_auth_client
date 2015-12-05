from os import environ
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask.ext.cors import CORS
import re
from httplib2 import Http
from oauth2client import client as oauth_client
import requests
import logging
from base64 import urlsafe_b64encode


SERVICE_URL = environ.get('SERVICE_URL', 'https://auth.api.beta.globus.org')


app = Flask(__name__)
CORS(app)
app.config.update(dict(
    PREFERRED_URL_SCHEME = "https"
))
app.config['DEBUG'] = environ.get('DEBUG', False)
app.secret_key = environ.get('SECRET_APPLICATION_KEY')

logging.basicConfig(level=logging.DEBUG)


def establishFlow():
    scope = environ['SCOPE_ID']
    client_id = environ['OAUTH_CLIENT_ID']
    basic_auth_str = urlsafe_b64encode("{}:{}".format(environ['OAUTH_CLIENT_ID'],
                                                      environ['OAUTH_CLIENT_SECRET']))
    auth_header = "Basic " + basic_auth_str
    with app.app_context():
        redirect_uri = url_for("profile", _external=True, _scheme="https")
    auth_uri = SERVICE_URL + "/authorize"
    token_uri = SERVICE_URL + "/token"

    return oauth_client.OAuth2WebServerFlow(client_id,
                                            scope=scope,
                                            authorization_header=auth_header,
                                            redirect_uri=redirect_uri,
                                            auth_uri=auth_uri,
                                            token_uri=token_uri)


@app.route("/")
def hello():
    session.pop('token', None)
    session.pop('access', None)
    auth_url = establishFlow().step1_get_authorize_url()
    return render_template("hello.html", auth_url=auth_url)


@app.route("/profile")
def profile():
    if 'token' in session:
        return render_template("profile.html", profile_data=session['token'],
                               access_token=session['access'],
                               resource_server=session['resource_server'],
                               other_tokens=session['other_tokens'])

    flow = establishFlow()
    auth_url = flow.step1_get_authorize_url()
    if "error" not in request.args and "code" not in request.args:
        if request.args:
            # Malformed response
            login_error = "Malformed Response"
            login_error_desc = "Please contact your login provider. We were unable to process their response."
            return render_template("login_error.html", login_error=login_error,
                                   login_error_desc=login_error_desc,
                                   auth_url=auth_url), 400
        # User went directly to /profile, prompt for login
        return render_template("need_login.html", auth_url=auth_url), 401
    if "error" in request.args:
        login_error = request.args.get("error")
        login_error_desc = "" if "error_description" not in request.args else request.args.get("error_description")
        return render_template("login_error.html", login_error=login_error,
                               login_error_desc=login_error_desc,
                               auth_url=auth_url), 401
    auth_code = request.args.get('code')
    h = Http(disable_ssl_certificate_validation=True)
    try:
        result = flow.step2_exchange(auth_code, http=h)
    except oauth_client.Error as err:
        return render_template("login_error.html", login_error=str(err),
                               auth_url=auth_url), 401
    else:
        session['token'] = result.id_token
        session['access'] = result.access_token
        session['resource_server'] = result.token_response['resource_server']
        session['other_tokens'] = result.token_response['other_tokens']
        return render_template("profile.html", profile_data=result.id_token,
                               access_token=result.access_token,
                               resource_server=result.token_response['resource_server'],
                               other_tokens=result.token_response['other_tokens'])


@app.route("/profile/api_expo")
def profile_api_expo():
    if 'access' not in session:
        return redirect(url_for('profile'))
    else:
        return render_template("profile_api_expo.html",
                               bearerToken=session['access'])


@app.route("/logout")
def logout():
    if 'access' in session:
        headers = { "Authorization": "Bearer {}".format(session['access']) }
        r = requests.delete(SERVICE_URL + "/token_details", headers=headers);
    session.pop('access', None)
    session.pop('token', None)
    session.pop('resource_server', None)
    session.pop('other_tokens', None)
    return redirect(url_for('hello'))


# Proxy routes
@app.route("/p/<path:url>", methods=['GET', 'POST', 'OPTIONS', 'DELETE'])
def proxy(url):
    if 'access' not in session:
        return redirect(url_for('profile'))
    else:
        target = SERVICE_URL + "/{}".format(url)
        headers = { "Authorization": "Bearer {}".format(session['access']) }
        r = requests.request(request.method, target, headers=headers, params=request.args)

        if re.search('json', r.headers.get('content-type')):
            return jsonify(r.json())
        return r.content


if __name__ == "__main__":
    app.run(port=int(environ.get('PORT')))
