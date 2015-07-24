from os import environ
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("hello.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/oauth2callback")
def oauth2callback():
    print "yup"
    return "Hello OAuth"

if __name__ == "__main__":
    app.run()
