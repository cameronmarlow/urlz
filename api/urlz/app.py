# -*- coding: utf-8 -*-
"""Blueprint for api server"""

from flask import Flask
from flask.ext.appconfig import AppConfig
from flask.ext.mail import Mail
from flask.ext.uuid import FlaskUUID
from flask.ext.security import Security
from urlz.sites import api

def create_app():
    app = Flask('urlz')

    # Initialize configuration (maybe make prefix relative?)
    AppConfig(app)

    # Initialize sql, login manager
    from urlz.model import db, user_datastore
    db.init_app(app)

    security = Security(app, user_datastore)
    app.db = db
    mail = Mail(app)

    # Initialize uuid
    flask_uuid = FlaskUUID()
    flask_uuid.init_app(app)

    # Add Blueprints
    app.register_blueprint(api, url_prefix='/api')

    return app

def create_local_app():
    """Create an app environment suitable for working locally"""
    app = urlz.app.create_app()
    app.test_request_context().push()
    return app
