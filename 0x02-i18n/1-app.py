#!/usr/bin/env python3
"""Basic babel setup"""

from flask_babel import Babel
from flask import request
app = __import__("0-app").app

babel = Babel(app=app)


class Config(object):
    """Configuration for babel"""
    LANGUAGES = ["en", "fr"]
    TIMEZONE = "UTC"


config = Config()
babel.default_locale = config.LANGUAGES[0]
babel.default_timezone = config.TIMEZONE
