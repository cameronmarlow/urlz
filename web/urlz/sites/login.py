# -*- coding: utf-8 -*-
"""Flask Blueprints for API"""

from flask import Blueprint, abort, request, jsonify
from flask.ext.security.utils import verify_password

from urlz.model import User

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User.query.filter_by(email=username).first()
    if user is None:
        # User not found
        abort(400)
    if verify_password(password, user.password):
        return jsonify({
            'username': user.username,
            'auth_token': user.get_auth_token()
        })
    else:
        abort(400)
