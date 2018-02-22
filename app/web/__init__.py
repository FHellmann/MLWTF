#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask_bootstrap import Bootstrap


def register_blueprints(app):
    Bootstrap(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint, url_prefix='/settings')
