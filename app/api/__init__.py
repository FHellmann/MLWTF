#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
from flask import Blueprint
from flask_restplus import Api
from app.api.api_rf import ns_rf
from app.api.api_dht import ns_dht

_LOGGER = logging.getLogger(__name__)

rest_api = Blueprint('api', __name__)

api = Api(
    rest_api,
    version='0.2',
    title='My Smart Home - Rest API',
    description='The rest api allows to access all the sensor data and control the actuators.',
    contact_email='info@fabio-hellmann.de'
)
api.add_namespace(ns_rf)
api.add_namespace(ns_dht)


@api.errorhandler
def default_error_handler(e: Exception):
    _LOGGER.exception('An unhandled exception occurred.')


def register_blueprints(app):
    app.register_blueprint(rest_api, url_prefix='/api')
