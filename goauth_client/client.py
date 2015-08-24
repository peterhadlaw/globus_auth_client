from os import environ
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import json
from httplib2 import Http
from oauth2client import client as oauth_client
import requests


app = Flask(__name__)
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
    auth_uri = "https://auth.api.globusauthtest.globuscs.info/authorize"
    token_uri = "https://auth.api.globusauthtest.globuscs.info/token"

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


@app.route("/profile/api_expo", methods=['GET', 'POST'])
def profile_api_expo():
    if 'access' not in session:
        return redirect(url_for('profile'))
    else:
        url = "https://auth.api.globusauthtest.globuscs.info"
        headers = {'Authorization': 'Bearer {}'.format(session['access'])}

        if request.method == 'POST':
            # API Explorer was used, let's process the request
            print "hey"
        #     path = request.form['path'] # required
        #     body = request.form.get(body, "")
        #     method = request.form['method']
        #     test_api_explorer = json.dumps(json.loads(requests.request(method, url + path, data=body, verify=False,
        #                      headers=headers).text), indent=2)
        # else:
        #     test_api_explorer = "No request processed. Please use API explorer."

        token_details_path = "/token_details"
        test_token_details = requests.get(url + token_details_path, verify=False,
                                     headers=headers)

        identities_path = "/identities"
        test_identities = requests.get(url + identities_path, verify=False,
                                  headers=headers)

        test_results = {
            'token_details': json.dumps(json.loads(test_token_details.text),
                                        indent=2),
            'identities': json.dumps(json.loads(test_identities.text),
                                     indent=2),
            'test_api_explorer': test_api_explorer
        }

        return render_template("profile_api_expo.html", test_results=test_results)


@app.route("/logout")
def logout():
    session.pop('access', None)
    return redirect(url_for('hello'))


if __name__ == "__main__":
    app.run(port=int(environ.get('PORT')))
