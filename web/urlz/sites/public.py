# -*- coding: utf-8 -*-
"""Flask Blueprints for Public website"""

from flask import Blueprint, abort, request, jsonify, render_template

public_blueprint = Blueprint('public', __name__)

@public_blueprint.route('/')
def home():
    return render_template('base.jinja.html')
