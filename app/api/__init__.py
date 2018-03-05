#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
from flask import Blueprint
from flask_restplus import Api
from .api_rf import api_rf

_LOGGER = logging.getLogger(__name__)

rest_api = Blueprint('api', __name__)

api = Api(
    rest_api,
    version='0.1',
    title='My Smart Home - Rest API',
    description='The rest api allows to access all the sensor data and control the actuators.',
    contact_email='info@fabio-hellmann.de'
)

api.add_namespace(api_rf, path='/rf')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    _LOGGER.exception(message)


def register_blueprints(app):
    app.register_blueprint(api, url_prefix='/api')
