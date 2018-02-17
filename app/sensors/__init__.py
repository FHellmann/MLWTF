#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Blueprint

sensors = Blueprint('sensors', __name__)

from . import api
