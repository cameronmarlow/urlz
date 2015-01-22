# -*- coding: utf-8 -*-
"""Flask Blueprint for API"""

import json
from flask import Blueprint, abort, request, jsonify, url_for
from flask.ext.security.decorators import auth_token_required
from flask.ext.security.utils import encrypt_password, verify_password
from flask.ext.security.core import current_user

from urlz.model import db, Post, Tag, URL, User, user_datastore
from urlz.util import deduplicate_form

api = Blueprint('api', __name__)

@api.route('/post/', methods=['GET'])
@api.route('/post/<uuid:obj_id>/', methods=['GET'])
def post_get(obj_id=None):
    """API endpoint for posts"""
    if obj_id is not None:
        # convert from uuid -> str
        res_obj = Post.query.get_or_404(str(obj_id))
        if res_obj:
            res_obj = res_obj.as_dict()
    else:
        res_obj = {
            'results': [x.as_dict() for x in Post.query.limit(10)]
        }
    return jsonify(res_obj)
    abort(404)

@api.route('/post/', methods=['POST', 'PUT'])
@api.route('/post/<uuid:obj_id>/', methods=['DELETE', 'PUT'])
@auth_token_required
def post_edit(obj_id=None):
    if request.method == 'POST':
        url = request.json.get('url')
        print(url)
    if request.method == 'PUT':
        res_obj = Post.query.get_or_404(obj_id)
        res_obj.data.update(request.get_json())
        db.session.add(res_obj)
        db.session.commit()
    abort(400)

## Tag creation/search

@api.route('/tag/<uuid:tag_id>', methods=['GET'])
@auth_token_required
def tag_get(tag_id):
    tag = Tag.query.get_or_404(str(tag_id))
    return jsonify({
        'id': tag.id,
        'name': tag.name,
        'type': tag.type,
        'description': tag.description
    })

@api.route('/tag/', methods=['POST'])
@api.route('/tag/<uuid:tag_id>/', methods=['DELETE', 'PUT'])
@auth_token_required
def tag_edit(obj_id=None):
    if request.method == 'POST':
        name = request.json.get('name')
        type = request.json.get('type')
        description = request.json.get('description')
        tag = Tag(name=name,
                  name_normalized=deduplicate_form(name),
                  type=type,
                  description=description,
                  owner_id=current_user.id)
        db.session.add(tag)
        db.session.commit()
        return jsonify({'tag_id': tag.id}), 201,\
            {'Location': url_for('api.tag_get', tag_id=tag.id)}

    abort(400)

## User creation/lookup

@api.route('/user/<username>')
def user_get(username):
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify({
        "username": user.username
    })

@api.route('/user/', methods=['PUT', 'POST'])
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

    # encrypt password
    encrypted_password = encrypt_password(password)
    user = user_datastore.create_user(email=email,
                                      username=username,
                                      password=encrypted_password)
    db.session.commit()
    return jsonify({'username': user.username}), 201,\
        {'Location': url_for('api.user_get', username=user.username)}

# Authentication
@api.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        api_error("Username or password missing")
    user = User.query.filter_by(username=username).first()
    if verify_password(password, user.password):
        return jsonify({
            'username': user.username,
            'auth_token': user.get_auth_token()
        })
    else:
        api_error("Password mismatch")

# Error Handlers

@api.errorhandler(400)
def api_error(error=None):
    """Custom error response for API issues"""
    response = {
        'code': 400,
        'message': 'The current API request could not be processed'
    }
    if error:
        response['message'] = str(error)

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
