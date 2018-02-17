#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Blueprint

actuators = Blueprint('actuators', __name__)

from . import api
