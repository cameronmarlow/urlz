# -*- coding: utf-8 -*-
"""Flask Blueprint for API"""

import json
from flask import Blueprint, abort, request, jsonify, current_app
from flask.ext.security.decorators import auth_token_required
from urlz.model import db, Post, Tag, URL, User, user_datastore

api = Blueprint('api', __name__)

@api.route('/post/', methods=['GET'])
@api.route('/post/<uuid:obj_id>/', methods=['GET'])
def post_get(obj_id=None):
    """API endpoint for posts"""
    # convert from uuid -> str
    obj_id = str(obj_id)
    if obj_id:
        if request.method == 'GET':
            res_obj = Post.query.get_or_404(obj_id)
        elif request.method == 'PUT':
            res_obj = Post.query.get_or_404(obj_id)
            res_obj.data.update(request.get_json())
            db.session.add(res_obj)
            db.session.commit()
        if res_obj:
            res_obj = res_obj.as_dict()
    else:
        if request.method == 'GET':
            res_obj = {
                'results': [x.as_dict() for x in Post.query.limit(10)]
            }

    return jsonify(res_obj)
    abort(404)


@api.route('/post/', methods=['POST', 'PUT'])
@api.route('/post/<uuid:obj_id>/', methods=['DELETE', 'PUT'])
@auth_token_required
def post_edit(obj_id=None):
    abort(400)

@api.route('/user/<username>')
def user_get(username):
    user = User.query.get_or_404(username=username)

@api.route('/user/', methods=['PUT'])
def user_create():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if username is None or password is None or email is None:
        # Username/password/email missing
        api_error("Username, password or email missing")
    if User.query.filter_by(username=username).first() is not None:
        # Username exists
        api_error("Username exists")

    user_datastore.create_user(email=email, username=username)
    db.session.commit()

# Error Handlers

@api.errorhandler(400)
def api_error(error=None):
    """Custom error response for API issues"""
    response = {
        'code': 400,
        'message': 'The current API request could not be processed'
    }
    if error:
        response['message'] = error

    return jsonify(response)

@api.errorhandler(404)
def not_found(error=None):
    """Custom error response for API 404"""
    response = {
        'code': 404,
        'message': 'Interface not defined for given URL'
    }
    if error:
        response['message'] = error
    return jsonify(response)
