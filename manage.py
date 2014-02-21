#!env/bin/python
# -*- coding: utf-8 -*-

from flask import *
from config import SQLALCHEMY_DATABASE_URI, VERSION_ACTUAL

from flask.ext.script import Manager, Command, Server
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db



class InfoCommand(Command):
    "prints app info"

    def run(self):
        print "Current site version: " + VERSION_ACTUAL
        print "Database URI: " + SQLALCHEMY_DATABASE_URI
        print "Satabase engine: " + db.engine.dialect.name


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.add_command('info', InfoCommand)

manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()