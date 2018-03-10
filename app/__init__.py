#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .api import register_blueprints as rest_api
from .web import register_blueprints as web_app

app = Flask(__name__, static_url_path='/app', static_folder='web/static', template_folder='web/templates')

rest_api(app)
web_app(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' # In-Memory usage for testing
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'my-smart-home.db')
db = SQLAlchemy(app)
