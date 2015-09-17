from os import environ
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask.ext.cors import CORS
import json
from httplib2 import Http
from oauth2client import client as oauth_client
import requests


app = Flask(__name__)
CORS(app)
app.config.update(dict(
    PREFERRED_URL_SCHEME = "https"
))
app.config['DEBUG'] = environ.get('DEBUG', False)
app.secret_key = environ.get('SECRET_APPLICATION_KEY')


def establishFlow():
    scope = environ['SCOPE_ID']
    client_id = environ['OAUTH_CLIENT_ID']
    auth_header = "Bearer " + environ['OAUTHORIZATION_TOKEN']
    with app.app_context():
        redirect_uri = url_for("profile", _external=True, _scheme="https")
    auth_uri = "https://auth.api.beta.globus.org/authorize"
    token_uri = "https://auth.api.beta.globus.org/token"

    return oauth_client.OAuth2WebServerFlow(client_id,
                                            scope=scope,
                                            authorization_header=auth_header,
                                            redirect_uri=redirect_uri,
                                            auth_uri=auth_uri,
                                            token_uri=token_uri)


@app.route("/")
def hello():
    auth_url = establishFlow().step1_get_authorize_url()
    return render_template("hello.html", auth_url=auth_url)


@app.route("/profile")
def profile():
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
        session['access'] = result.access_token
        return render_template("profile.html", profile_data=result.id_token)


@app.route("/profile/api_expo")
def profile_api_expo():
    if 'access' not in session:
        return redirect(url_for('profile'))
    else:
        return render_template("profile_api_expo.html",
                               bearerToken=session['access'])


@app.route("/logout")
def logout():
    session.pop('access', None)
    return redirect(url_for('hello'))


# Proxy routes
@app.route("/p/<path:url>", methods=['GET', 'POST', 'OPTIONS', 'DELETE'])
def proxy(url):
    if 'access' not in session:
        return redirect(url_for('profile'))
    else:
        target = "https://auth.api.beta.globus.org/{}".format(url)
        headers = { "Authorization": "Bearer {}".format(session['access']) }
        r = requests.request(request.method, target, headers=headers, params=request.args)
        return r.content



if __name__ == "__main__":
    app.run(port=int(environ.get('PORT')))
