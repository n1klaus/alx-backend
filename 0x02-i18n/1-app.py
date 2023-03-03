#!/usr/bin/env python3
"""Basic babel setup"""

from flask_babel import Babel
from flask import Flask, render_template


class Config(object):
    """Configuration for babel"""
    LANGUAGES = ["en", "fr"]
    TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app=app, default_locale=app.config["LANGUAGES"][0],
              default_timezone=app.config["TIMEZONE"])


@app.route("/", strict_slashes=False)
def root():
    """Root page"""
    return render_template("1-index.html")


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000
    app.run(host=HOST, port=PORT)
