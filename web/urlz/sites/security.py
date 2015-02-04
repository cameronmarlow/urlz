# -*- coding: utf-8 -*-
"""Extensions for Flask-Security"""

from flask.ext.security.forms import ConfirmRegisterForm, LoginForm
from wtforms import TextField
from wtforms.validators import Required

class ExtendedRegisterForm(ConfirmRegisterForm):
    username = TextField('Username', [Required()])

class LoginBothForm(LoginForm):
    email = TextField('Email address or username', [Required()])