#!env/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request, send_from_directory, make_response
from app import app, db
from flask.ext.admin import AdminIndexView, form
from flask.ext.admin.base import expose
from flask.ext.login import current_user, login_required
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.base import BaseView


from email.mime.text import MIMEText
import smtplib
import git

import datetime
from werkzeug.contrib.cache import SimpleCache

from sqlalchemy import func

from config import UPLOADS_DIR, SMTP_HOST, SMTP_USER, SMTP_PASS, SMTP_PORT, SMTP_TLS, EMAIL_SUBJECT, CONTACT_TO
import os
import urllib
import json
import re
from jinja2 import Markup

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>¿?@\[\\\]^_`{|},.]+')

cache = SimpleCache()


def slugify(value, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(value.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))


app.jinja_env.filters['slugify'] = slugify


@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)


@app.route('/')
@app.route('/index/')
def index(id=None, slug=None):
    return render_template("index.html")



@app.route('/humans.txt')
def humans():

    _PATH = os.path.abspath(os.path.dirname(__file__))

    try:
        repo = git.Repo(os.path.join(os.path.dirname(_PATH)))
        fecha = datetime.datetime.fromtimestamp(
            repo.head.reference.commit.committed_date)
        autor = repo.head.reference.commit.author.name

    except:
        repo = False
        fecha = False
        autor = False

    response = make_response(render_template(
        "humans.txt", repo=repo, fecha=fecha, autor=autor, path=_PATH))

    response.headers['Content-Type'] = "text/plain; charset=utf-8"

    return response

# para servir archivos estáticos

@app.route('/robots.txt')
# @app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/favicon.ico')
# @app.route('/sitemap.xml')
def favicon():
    return send_from_directory(os.path.join(app.static_folder, 'img'), request.path[1:])

# Views Admin


class MyAdminIndexView(AdminIndexView):

    @expose("/")
    @login_required
    def index(self):
        return self.render("admin_local/index.html")


class LogoutView(BaseView):

    @expose("/")
    def logout(self):
        return redirect(url_for("usuarios.logout"))
