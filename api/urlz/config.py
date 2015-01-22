# -*- coding: utf-8 -*-
"""Non-sensitive settings"""

class Config(object):
    """Default config object"""
    # Mail
    MAIL_USE_TLS = True

    # Security
    SECURITY_EMAIL_SENDER = "no-reply@urlz.co"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True

    HTTP_PORT = 6060
