from os import environ
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from httplib2 import Http
from oauth2client import client as oauth_client


app = Flask(__name__)

app.config.update(dict(
    PREFERRED_URL_SCHEME = "https"
))


def establishFlow():
    scope = environ['SCOPE_ID']
    client_id = environ['OAUTH_CLIENT_ID']
    auth_header = "Bearer " + environ['OAUTHORIZATION_TOKEN']
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
        return render_template("need_login.html", auth_url=auth_url), 401
    if "error" in request.args:
        login_error = request.args.get("error")
        login_error_desc = "" if "error_description" not in request.args else request.args.get("error_description")
        return render_template("login_error.html", login_error=login_error,
                               login_error_desc=login_error_desc,
                               auth_url=auth_url), 401
    auth_code = request.args.get('code')
    h = Http(disable_ssl_certificate_validation=True)
    result = flow.step2_exchange(auth_code, http=h)
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)
