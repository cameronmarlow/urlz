# -*- coding: utf-8 -*-
"""Application specification for urlz api."""

from flask import Flask
from flask.ext.appconfig import AppConfig

app = Flask('urlz')
AppConfig(app)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)