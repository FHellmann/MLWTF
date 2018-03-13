#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging

from flask import Flask
from flask_bootstrap import Bootstrap

from config import app_config
from .database import db

_LOGGER = logging.getLogger(__name__)


def create_app(config_name):
    _LOGGER.info("Setup flask app with env=" + str(config_name))

    # Initialise flask and database
    app = Flask(__name__, static_url_path='/app', static_folder='web/static', template_folder='web/templates')
    app.config.from_object(app_config[config_name])

    db_path = app.config['DATABASE_URI']
    db.setup(db_path)

    Bootstrap(app)

    # Logging
    app.logger.addHandler(app.config['LOG_HANDLER'])

    # Setup web app and rest api
    from .web import register_blueprints as web_app
    web_app(app)

    from .api import register_blueprints as rest_api
    rest_api(app)

    _LOGGER.info("Flask app is ready")

    return app
