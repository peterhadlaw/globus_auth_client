from os import environ
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from oauth2client import client as oauth_client


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("hello.html")

@app.route("/auth")
def auth():
    scope = "profile"
    client_id = environ['OAUTH_CLIENT_ID']
    client_secret = environ['OAUTH_CLIENT_SECRET']
    redirect_uri = url_for("oauth2callback")
    flow = oauth_client.OAuth2WebServerFlow(client_id, client_secret, scope,
                                            redirect_uri = redirect_uri)
    auth_url = flow.step1_get_authorize_url()
    return redirect(location=auth_url)


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/oauth2callback")
def oauth2callback():
    print "yup"
    return "Hello OAuth"

if __name__ == "__main__":
    app.run()
