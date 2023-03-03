#!/usr/bin/env python3
"""Flask with babel"""

from flask_babel import Babel
from flask import Flask, g, render_template, request


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """Configuration for babel"""
    LANGUAGES = ["en", "fr"]

    BABEL_DEFAULT_LOCALE = LANGUAGES[0]
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app=app)


@babel.localeselector
def get_locale():
    """Returns best matching locale according to language weights"""
    locale: str = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.before_request
def before_request():
    """"""
    user = get_user()
    if user:
        g.user = user


def get_user():
    """"""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except BaseException:
        return None


@app.route("/", strict_slashes=False)
def root():
    """Root page"""
    return render_template("5-index.html")


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000
    app.run(host=HOST, port=PORT)
