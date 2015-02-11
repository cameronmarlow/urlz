# -*- coding: utf-8 -*-
"""Flask Blueprints for Public website"""

from flask import Blueprint, abort, request, jsonify, render_template, flash
from flask.ext.security.core import current_user
from flask.ext.wtf import Form
from urlz.model import Tag, URL, Post, db

from wtforms import StringField, SelectField, SubmitField, HiddenField, validators

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/user/<username>')
def profile(username):
    return render_template('user/profile.jinja.html', username=username)

class PostForm(Form):
    owner_id = HiddenField('Owner ID')
    url = StringField('URL')
    url_id = HiddenField('URL ID', [validators.required()])
    category = SelectField('Category')
    # ccs = SelectField('CCs')
    note = StringField('Comment')
    submit = SubmitField('Submit')

@users_blueprint.route('/post', methods=['GET', 'POST'])
def post():
    url = request.args.get('url')
    post_url = None
    posted = False

    # Build post form
    form = PostForm()
    tags = Tag.query.filter_by(owner_id=current_user.id).all()
    form.category.choices = [(tag.id, tag.name) for tag in tags]

    if form.validate_on_submit():
        url_id = form.data.get('url_id')
        post_url = URL.query.filter_by(id=url_id).first()
        post = Post(
            owner_id=form.data.get('owner_id'),
            canonical_url=url_id,
            note=form.data.get('note'),
        )
        if form.data.get('category'):
            tag_lookup = dict([(tag.id, tag) for tag in tags])
            post.tags.append(tag_lookup[form.data.get('category')])
        db.session.add(post)
        db.session.commit()
        posted = True
        flash('URL posted successfully')

    if url:
        # Check to see if URL exists, if not add it for preview
        post_url = URL.query.filter_by(url=url).first()
        if not post_url:
            post_url = URL(url=url)
            db.session.add(post_url)
            db.session.commit()
        form.url.data = post_url.url
        form.url_id.data = post_url.id
        form.owner_id.data = current_user.id

    return render_template(
        'user/post.jinja.html',
        post_form=form,
        url=url,
        url_preview=post_url,
        posted=posted)

