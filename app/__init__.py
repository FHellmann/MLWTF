#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Flask


def create_app():
    app = Flask(__name__, static_url_path='/app', static_folder='web/static', template_folder='web/templates')

    from .api import register_blueprints as rest_api
    rest_api(app)

    from .web import register_blueprints as web_app
    web_app(app)

    return app
