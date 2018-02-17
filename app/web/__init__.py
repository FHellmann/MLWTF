#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    Bootstrap(app)

    from app.web.settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint, url_prefix='/settings')

    from app.web.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
