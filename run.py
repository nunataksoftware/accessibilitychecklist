#!env/bin/python
# -*- coding: utf-8 -*-

from app import app
app.run(debug=app.debug, host="0.0.0.0")
