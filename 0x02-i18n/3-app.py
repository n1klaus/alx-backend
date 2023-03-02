#!/usr/bin/env python3
"""Flask with babel"""

from flask import request, Flask, render_template
from flask_babel import Babel, _

app = Flask(__name__)

babel = Babel(app=app)


class Config(object):
    """Configuration for babel"""
    LANGUAGES = ["en", "fr"]
    TIMEZONE = "UTC"


config = Config()


@babel.localeselector
def get_locale():
    """Returns best matching locale according to language weights"""
    return request.accept_languages.best_match(config.LANGUAGES)


@babel.timezoneselector
def get_timezone():
    """Sets the timezone for the app"""
    return config.TIMEZONE


@app.route("/", strict_slashes=False)
def home():
    """Home page"""
    return render_template("3-index.html",
                           home_title=_("Welcome to Holberton"),
                           home_header=_("Hello world"))


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000
    app.run(host=HOST, port=PORT)
