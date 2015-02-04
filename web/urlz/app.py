# -*- coding: utf-8 -*-
"""Blueprint for api server"""

from flask import Flask
from flask.ext.appconfig import AppConfig
from flask.ext.mail import Mail
from flask.ext.uuid import FlaskUUID
from flask.ext.security import Security
from flask.ext.bootstrap import Bootstrap


from urlz.sites.api import API
from urlz.sites.login import login_blueprint
from urlz.sites.public import public_blueprint
from urlz.sites.users import users_blueprint
from urlz.sites.security import ExtendedRegisterForm

from urlz.config import Config

def create_app():
    app = Flask('urlz',
                static_folder='../resources/static',
                template_folder='../resources/templates')

    # Initialize configuration (maybe make prefix relative?)
    app.config.from_object(Config)
    AppConfig(app)

    Bootstrap(app)

    # Initialize sql, login manager
    from urlz.model import db, user_datastore
    db.init_app(app)

    security = Security(app,
                        user_datastore,
                        confirm_register_form=ExtendedRegisterForm)
    app.db = db
    mail = Mail(app)

    # Initialize uuid
    flask_uuid = FlaskUUID()
    flask_uuid.init_app(app)

    api = API(app)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(public_blueprint)
    app.register_blueprint(users_blueprint)
    return app

def create_local_app():
    """Create an app environment suitable for working locally"""
    app = create_app()
    app.test_request_context().push()
    return app
