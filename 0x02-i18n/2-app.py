#!/usr/bin/env python3
"""Basic flask app"""

from flask_babel import Babel
from flask import request
app = __import__("0-app").app

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
