#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""


def register_blueprints(app):
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint, url_prefix='/settings')
