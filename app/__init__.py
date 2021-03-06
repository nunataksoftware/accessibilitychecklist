#!env/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin

from config import UPLOADS_DIR, USERUPLOADS_DIR, LANGUAGES
from flask.ext.babelex import Babel


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.login_message = ""

# @app.errorhandler(404)


def not_found(error):
    return render_template('404.html'), 404

from app.users.views import users
from app.users.models import User
from app.users.views import UserView

#from app.checklist.views import users
from app.checklist.models import Principle, PrinciplesTranslation

app.register_blueprint(users)
#app.register_blueprint(pages)
#app.register_blueprint(checklist)

from app.views import *
#from app.models import *

# Flask-Admin Configuration
admin = Admin(app, index_view=MyAdminIndexView())

# Create directories to upload files
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

if not os.path.exists(USERUPLOADS_DIR):
    os.makedirs(USERUPLOADS_DIR)

admin.add_view(ModelView(Principle, db.session, name='Principles'))
admin.add_view(ModelView(PrinciplesTranslation, db.session, name='Principles Translation'))
admin.add_view(UserView(db.session, "Users"))

# File-Manager Configuration
admin.add_view(
    FileAdmin(USERUPLOADS_DIR, '/static/uploads/useruploads/', name='Files'))

admin.add_view(LogoutView(name="Logout"))

# For Translations

babel = Babel(app)


@babel.localeselector
def get_locale():
    # We should get this from the config, but it fails, the same happens with timezone
    #return "es"
    return request.accept_languages.best_match(LANGUAGES.keys())


def get_timezone():
    return "America/Argentina/Mendoza"
