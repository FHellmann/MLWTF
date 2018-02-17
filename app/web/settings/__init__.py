#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Blueprint

settings = Blueprint('settings', __name__)

from . import views
