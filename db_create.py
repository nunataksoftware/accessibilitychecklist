#!env/bin/python
# -*- coding: utf-8 -*-

from flask import *
from app import *
from config import SQLALCHEMY_DATABASE_URI

from app import db

print "Creating database on: " + SQLALCHEMY_DATABASE_URI

db.create_all()

from app.users.models import User
from werkzeug.security import generate_password_hash


user_count = User.query.count()

if user_count == 0:
    """ We need at least one user """
    user = "root"
    password = "root"
    root = User(
        username=user,
        password=generate_password_hash(password)
    )

    db.session.add(root)
    db.session.commit()

    print "Superuser created: " + user + " - " + password
