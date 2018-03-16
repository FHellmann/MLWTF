#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import os
import logging
import logging.config
import yaml

from flask import Flask
from flask_bootstrap import Bootstrap

from enum import Enum, unique

from .database import db
from .core.scheduler import scheduler

_LOGGER = logging.getLogger(__name__)


@unique
class Environment(Enum):
    PRODUCTION = 'production'
    DEVELOPMENT = 'development'
    TESTING = 'testing'


class Config(object):
    def __init__(self, environment=Environment.PRODUCTION, default_path='config.yaml', env_key='CFG'):
        self.env = environment
        self.path = default_path
        self.value = os.getenv(env_key, None)
        self.config = None

        self.load()

    def load(self):
        if self.value:
            self.path = self.value
        if os.path.exists(self.path):
            with open(self.path, 'rt') as f:
                self.config = yaml.safe_load(f.read())

    def logging(self):
        return self._get_config_part('logging')

    def database(self):
        return self._get_config_part('database')

    def _get_config_part(self, name):
        if not(self.config is None):
            return self.config[name][self.env.value]


def create_app(env_name):
    config = Config(environment=Environment(env_name) if not(env_name is None) else Environment.PRODUCTION)

    _LOGGER.info("Setup flask app with env=" + str(env_name))

    # Initialise flask and database
    app = Flask(__name__, static_url_path='/app', static_folder='web/static', template_folder='web/templates')

    db_path = config.database()['uri']
    db.setup(db_path)

    Bootstrap(app)

    # Logging
    logging.config.dictConfig(config.logging())

    # Setup web app and rest api
    from .web import register_blueprints as web_app
    web_app(app)

    from .api import register_blueprints as rest_api
    rest_api(app)

    _LOGGER.info("Flask app is ready")

    scheduler.start()

    return app
