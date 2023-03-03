#!/usr/bin/env python3
"""Basic flask app"""

from flask_babel import Babel
from flask import Flask, render_template, request


class Config(object):
    """Configuration for babel"""
    LANGUAGES = ["en", "fr"]
    TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app=app)


@babel.localeselector
def get_locale():
    """Returns best matching locale according to language weights"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """Sets the timezone for the app"""
    return app.config["TIMEZONE"]


@app.route("/", strict_slashes=False)
def root():
    """Root page"""
    return render_template("2-index.html")


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000
    app.run(host=HOST, port=PORT)
