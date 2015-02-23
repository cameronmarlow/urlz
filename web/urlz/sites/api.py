# -*- coding: utf-8 -*-
"""Flask Blueprints for API"""

import json
from flask import Blueprint, abort, request, jsonify, url_for
from flask.ext.security.decorators import _check_token
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.security.core import current_user
from flask.ext.restless import APIManager, ProcessingException


from urlz.model import db, Post, Tag, URL, User, AddressBook, user_datastore

def user_encrypt_password(data=None, **kw):
    """Encrypt a user password before storing in the database"""
    if 'password' in data:
        data['password'] = encrypt_password(data['password'])

def check_auth(**kw):
    _check_token()
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not authenticated!',
            code=401)
    return True

def check_owner(data=None, **kw):
    """Check to make sure the owner of an object is updating/deleting it"""
    if data and 'owner_id' in data and not data['owner_id'] == current_user.id:
        raise ProcessingException(description="No write privileges",
            code=401)

def add_owner_id(data=None, **kw):
    """Add owner_id to tag"""
    data['owner_id'] = current_user.id

class API(object):

    def __init__(self, app):
        self.app = app
        self.manager = APIManager(app, flask_sqlalchemy_db=db)
        self.generate_blueprints()

    def generate_blueprints(self):
        """Generate blueprints for API usage"""
        user_blueprint = self.manager.create_api_blueprint(
            User,
            methods=['GET', 'POST', 'PATCH', 'DELETE'],
            primary_key='username',
            include_columns=['name', 'username', 'tags', 'posts'],
            preprocessors=dict(
                GET_SINGLE=[check_auth],
                GET_MANY=[check_auth],
                POST=[user_encrypt_password],
                PATCH_SINGLE=[check_auth, user_encrypt_password, check_owner],
                DELETE=[check_auth, check_owner]
            )
        )
        self.app.register_blueprint(user_blueprint)

        tag_blueprint = self.manager.create_api_blueprint(
            Tag,
            methods=['GET', 'POST', 'PATCH', 'DELETE'],
            preprocessors=dict(
                GET_SINGLE=[check_auth],
                GET_MANY=[check_auth],
                POST=[check_auth, add_owner_id, check_owner],
                PATCH_SINGLE=[check_auth, check_owner],
                DELETE=[check_auth, check_owner]
            )
        )
        self.app.register_blueprint(tag_blueprint)

        post_blueprint = self.manager.create_api_blueprint(
            Post,
            methods=['GET', 'POST', 'PATCH', 'DELETE'],
            preprocessors=dict(
                GET_SINGLE=[check_auth],
                GET_MANY=[check_auth],
                POST=[check_auth, check_owner, add_owner_id],
                PATCH_SINGLE=[check_auth, check_owner],
                DELETE=[check_auth, check_owner]
            )

        )
        self.app.register_blueprint(post_blueprint)

        url_blueprint = self.manager.create_api_blueprint(
            URL,
            methods=['GET', 'POST'],
            preprocessors=dict(
                GET_SINGLE=[check_auth],
                GET_MANY=[check_auth],
                POST=[check_auth]
            )
        )
        self.app.register_blueprint(url_blueprint)


        addressbook_blueprint = self.manager.create_api_blueprint(
            AddressBook,
            methods=['GET', 'POST'],
            preprocessors=dict(
                GET_SINGLE=[check_auth],
                GET_MANY=[check_auth],
                POST=[check_auth, check_owner, add_owner_id],
                PATCH_SINGLE=[check_auth, check_owner],
                DELETE=[check_auth, check_owner]
            )
        )
        self.app.register_blueprint(addressbook_blueprint)

