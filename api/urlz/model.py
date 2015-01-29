"""Models for SQL Datastore"""

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import UniqueConstraint
from flask.ext.security import SQLAlchemyUserDatastore, UserMixin, \
    RoleMixin

from urlz.util import deduplicate_form


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
    id = db.Column(UUID(), server_default=db.func.uuid_generate_v4(),
                   primary_key=True)

# Define models
role_user = db.Table(
    'role_user',
    db.Column('user_id', UUID(), db.ForeignKey('user.id')),
    db.Column('role_id', UUID(), db.ForeignKey('role.id')),
    db.Column('created_at', db.DateTime(), server_default=db.func.now()),
    db.Column('updated_at', db.DateTime(), server_default=db.func.now(), onupdate=db.func.current_timestamp())
)

class Role(IDMixin, AuditMixin, RoleMixin, db.Model):
    """User Role (admin, editor, etc.)"""
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(IDMixin, AuditMixin, UserMixin, db.Model):
    """User table"""
    __tablename__ = 'user'

    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(39))
    current_login_ip = db.Column(db.String(39))
    login_count = db.Column(db.Integer())
    roles = db.relationship('Role', secondary=role_user,
                            backref=db.backref('user', lazy='dynamic'))
    posts = db.relationship('Post')
    tags = db.relationship('Tag')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class URL(IDMixin, AuditMixin, db.Model):
    """General table for URLs"""
    __tablename__ = 'url'

    url = db.Column(db.String, unique=True, nullable=False)

# Post -> Tag assocation table
post_tag = db.Table(
    'post_tag',
    db.Column('post_id', UUID(), db.ForeignKey('post.id')),
    db.Column('tag_id', UUID(), db.ForeignKey('tag.id')),
    db.Column('created_at', db.DateTime(), server_default=db.func.now()),
    db.Column('updated_at', db.DateTime(), server_default=db.func.now(),
              onupdate=db.func.current_timestamp())
)

# Post -> CC association table
post_cc = db.Table(
    'post_cc',
    db.Column('post_id', UUID(), db.ForeignKey('post.id')),
    db.Column('user_id', UUID(), db.ForeignKey('user.id')),
    db.Column('created_at', db.DateTime(), server_default=db.func.now()),
    db.Column('updated_at', db.DateTime(), server_default=db.func.now(),
              onupdate=db.func.current_timestamp())
)

class Post(IDMixin, AuditMixin, db.Model):
    """The URL Post, in all its glory. Each post can be associated with tags
    (topics) and CCs (people to notify)"""
    __tablename__ = 'post'

    owner_id = db.Column(UUID(), db.ForeignKey('user.id'), nullable=False)
    canonical_url = db.Column(UUID(), db.ForeignKey('url.id'), nullable=False)
    note = db.Column(db.String)
    tags = db.relationship('Tag', secondary=post_tag,
                           backref=db.backref('post', lazy='dynamic'))
    ccs = db.relationship('User', secondary=post_cc)
    privacy = db.Column(db.Enum('private', 'public', name='post_privacy'),
                        default='public', nullable=False)

class Tag(IDMixin, AuditMixin, db.Model):
    """The Tag. A simple bucket for stuff."""
    __tablename__ = 'tag'

    owner_id = db.Column(UUID(), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    name_normalized = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('user', 'group', 'system', 'org',
                     name='tag_type'), nullable=False)
    description = db.Column(db.String(255))

    __table_args__ = (
        UniqueConstraint("owner_id", "type", "name_normalized",
                         name="user_tag_constraint"),
    )

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
        if self.name and not self.name_normalized:
            self.name_normalized = deduplicate_form(self.name)

class URLCache(AuditMixin, db.Model):
    """Cache for URLs"""
    __tablename__ = 'urlcache'

    url_id = db.Column(UUID, db.ForeignKey('url.id'),
                       primary_key=True,
                       nullable=False)
    headers = db.Column(JSON)
    status = db.Column(db.Enum('success', 'failure', name='url_status'),
                       default='success')
