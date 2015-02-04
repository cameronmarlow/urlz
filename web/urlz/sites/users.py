# -*- coding: utf-8 -*-
"""Flask Blueprints for Public website"""

from flask import Blueprint, abort, request, jsonify, render_template

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/user/<username>')
def profile(username):
    return render_template('user/profile.jinja.html', username=username)
