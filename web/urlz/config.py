# -*- coding: utf-8 -*-
"""Non-sensitive settings"""

class Config(object):
    """Default config object"""
    # Name
    SITE_NAME = 'URLer'

    # Mail
    MAIL_USE_TLS = True
    DEFAULT_MAIL_SENDER = 'Admin < username@example.com >'

    # Security
    SECURITY_EMAIL_SENDER = "no-reply@urlz.co"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('email', 'username')

    SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.jinja.html'
    SECURITY_REGISTER_USER_TEMPLATE = 'security/register_user.jinja.html'
    SECURITY_FORGOT_PASSWORD_TEMPLATE = 'security/forgot_password.jinja.html'
    SECURITY_SEND_CONFIRMATION_TEMPLATE = 'security/send_confirmation.jinja.html'

    HTTP_PORT = 6060
