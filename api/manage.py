# -*- coding: utf-8 -*-
"""Migrations manager"""

import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.appconfig import AppConfig
from urlz.app import create_local_app

app = create_local_app()
db = app.db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()