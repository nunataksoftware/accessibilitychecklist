#!env/bin/python
# -*- coding: utf-8 -*-
import os

_basedir = ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

ADMINS = frozenset(['gui.nunez@gmail.com'])

VERSION_ACTUAL = '1.0'

UPLOADS_DIR = os.path.join(_basedir, "app/static/uploads")
USERUPLOADS_DIR = UPLOADS_DIR
DEBUG = True
# DEBUG_TB_INTERCEPT_REDIRECTS = False
CSRF_ENABLED = True
CSRF_SESSION_KEY = "o4kgR09y0OG0x6jN600lAL7RVezf93i2"

SECRET_KEY = 'accesibilitychecklist-secret-key'  # To sign cookies
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(_basedir, 'database.db'))

THREADS_PER_PAGE = 8

BABEL_DEFAULT_LOCALE = "es"
BABEL_DEFAULT_TIMEZONE = "America/Argentina/Mendoza"

LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# Email

SMTP_HOST = 'mail.nunataksoftware.com'
SMTP_USER = 'test@nunataksoftware.com'
SMTP_PASS = 'sEcfCFPQ'
SMTP_PORT = 465
SMTP_TLS = True
EMAIL_SUBJECT = 'Test Email - Ignore: '
CONTACT_TO = 'info@nunataksoftware.com'


try:
    from config_local import *
except ImportError:
    pass
