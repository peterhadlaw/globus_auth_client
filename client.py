from os import environ
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from oauth2client import client as oauth_client


app = Flask(__name__)


def establishFlow():
    scope = "profile"
    client_id = environ['OAUTH_CLIENT_ID']
    client_secret = environ['OAUTH_CLIENT_SECRET']
    redirect_uri = url_for("oauth2callback", _external=True)

    return oauth_client.OAuth2WebServerFlow(client_id, client_secret, scope,
                                            redirect_uri=redirect_uri)


@app.route("/")
def hello():
    auth_url = establishFlow().step1_get_authorize_url()
    return render_template("hello.html", auth_url=auth_url)


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/oauth2callback")
def oauth2callback():
    if "error" in request.args:
        return "There was an authentication error: " + request.args.get("error")
    auth_code = request.args.get('code')
    result = establishFlow().step2_exchange(auth_code)
    print str(result)
    return "Hello OAuth:" + str(result)

if __name__ == "__main__":
    app.run()
