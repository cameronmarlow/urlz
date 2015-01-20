"""Models for SQL Datastore"""

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSON
from flask.ext.security import SQLAlchemyUserDatastore, UserMixin, \
    RoleMixin

# TODO: Privacy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define mixins
class AuditMixin(object):
    """Simple Mixin to provide timestamps"""
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), server_default=db.func.now(),
        onupdate=db.func.current_timestamp())

class IDMixin(object):
    """Mixin to provide standard ID types"""
    id = db.Column(UUID(), primary_key=True,
                   server_default=db.text("uuid_generate_v4()"))

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', UUID(), db.ForeignKey('users.id')),
    db.Column('role_id', UUID(), db.ForeignKey('roles.id')),
    db.Column('created_at', db.DateTime(), server_default=db.func.now()),
    db.Column('updated_at', db.DateTime(), server_default=db.func.now(), onupdate=db.func.current_timestamp())
)

class Role(db.Model, RoleMixin, AuditMixin, IDMixin):
    """User Role (admin, editor, etc.)"""
    __tablename__ = 'roles'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin, AuditMixin, IDMixin):
    """User table"""
    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(39))
    current_login_ip = db.Column(db.String(39))
    login_count = db.Column(db.Integer())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class URL(db.model, AuditMixin, IDMixin):
    """General table for URLs"""
    __tablename__ = 'urls'

    url = db.Column(db.String, unique=True)

# Post -> Tag assocation table
post_tags = db.Table(
    'posts_tags',
    db.Column('post_id', UUID(), db.ForeignKey('posts.id')),
    db.Column('tag_id', UUID(), db.ForeignKey('tags.id')),
    db.Column('created_at', db.DateTime(), server_default=db.func.now()),
    db.Column('updated_at', db.DateTime(), server_default=db.func.now(),
              onupdate=db.func.current_timestamp())
)

# Post -> CC association table
post_ccs = db.Table(
    'posts_ccs',
    db.Column('post_id', UUID(), db.ForeignKey('posts.id')),
    db.Column('user_id', UUID(), db.ForeignKey('users.id')),
    db.Column('created_at', db.DateTime(), server_default=db.func.now()),
    db.Column('updated_at', db.DateTime(), server_default=db.func.now(),
              onupdate=db.func.current_timestamp())
)

class Post(db.Model, IDMixin, AuditMixin):
    """The URL Post, in all its glory. Each post can be associated with tags
    (topics) and CCs (people to notify)"""
    __tablename__ = 'posts'

    url = db.Column(UUID(), db.ForeignKey('urls.id'))
    note = db.Column(db.String)
    tags = db.relationship('Tag', secondary=post_tags,
                           backref=db.backref('posts', lazy='dynamic'))
    ccs = db.relationship('User', secondary=post_ccs)

class Tag(db.Model, IDMixin, AuditMixin):
    """The Tag. A simple bucket for stuff."""
    __tablename__ = 'tags'

    owner_id = db.Column(UUID(), db.ForeignKey('users.id'))
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

class URLCache(db.Model, AuditMixin):
    """Cache for URLs"""
    __tablename__ = 'urlcache'

    url = db.Column(db.String, db.ForeignKey('urls.url'))
    headers = db.Column(JSON)
    status = db.Column(db.Enum('success', 'failure', name='url_status'),
                       default='success')
