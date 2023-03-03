#!/usr/bin/env python3
"""Basic flask app"""

from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def root():
    """Root page"""
    return render_template("0-index.html")


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 5000
    app.run(host=HOST, port=PORT)
