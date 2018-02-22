#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from .api import register_blueprints as rest_api
    rest_api(app)

    from .web import register_blueprints as web_app
    web_app(app)

    return app
