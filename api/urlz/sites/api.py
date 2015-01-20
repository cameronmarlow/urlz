# -*- coding: utf-8 -*-
"""Flask Blueprint for API"""

import json
from flask import Blueprint, abort, request, jsonify, current_app
from urlz.model import Post, Tag, URL, User

api = Blueprint('api', __name__)

@api.route('/post/', methods=['GET', 'POST', 'PUT'])
@api.route('/post/<uuid:obj_id>/', methods=['DELETE', 'GET', 'PUT'])
def post_handler(obj_id=None):
    """API endpoint for posts"""
    # convert from uuid -> str
    obj_id = str(obj_id)
    if obj_id:
        if request.method == 'GET':
            res_obj = Post.query.get_or_404(obj_id)
        elif request.method == 'PUT':
            res_obj = Post.query.get_or_404(obj_id)
            res_obj.data.update(request.get_json())
            res_obj.query.session.add(res_obj)
            res_obj.query.session.commit()
        if res_obj:
            res_obj = res_obj.as_dict()
    else:
        if request.method == 'GET':
            res_obj = {
                'results': [x.as_dict() for x in Post.query.limit(10)]
            }

    return jsonify(res_obj)
    abort(404)

# TODO: Tag Search, User
