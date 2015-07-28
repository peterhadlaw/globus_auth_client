from os import environ
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from oauth2client import client as oauth_client


app = Flask(__name__)


def establishFlow():
    scope = environ['SCOPE_ID']
    client_id = environ['OAUTH_CLIENT_ID']
    auth_header = "Bearer: " + environ['OAUTHORIZATION_TOKEN']
    redirect_uri = url_for("profile", _external=True)
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
    if "error" not in request.args and "code" not in request.args:
        return render_template("need_login.html"), 401
    if "error" in request.args:
        return "There was an authentication error: " + request.args.get("error")
    auth_code = request.args.get('code')
    result = establishFlow().step2_exchange(auth_code)
    return render_template("profile.html")


if __name__ == "__main__":
    app.run()
