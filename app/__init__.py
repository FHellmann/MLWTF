#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    Bootstrap(app)

    # Web App
    from .web.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .web.settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint, url_prefix='/settings')

    # Rest API for Sensors
    from .actuators import actuators as actuators_blueprint
    app.register_blueprint(actuators_blueprint, url_prefix='/api/actuators')

    # Rest API for Actuators
    from .sensors import sensors as sensors_blueprint
    app.register_blueprint(sensors_blueprint, url_prefix='/api/sensors')

    return app
