#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Flask

from .api import register_blueprints as rest_api
from .web import register_blueprints as web_app
from .database import setup as database

app = Flask(__name__, static_url_path='/app', static_folder='web/static', template_folder='web/templates')

rest_api(app)
web_app(app)
database(app)
