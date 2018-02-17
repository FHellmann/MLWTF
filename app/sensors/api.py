#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from . import sensors
from flask import request, abort


# Define services


# Define Rest Calls


@sensors.route('/', methods=['GET'])
def index():
    pass


@sensors.route('/rx/start', methods=['PUT'])
def rx_find():
    pass


@sensors.route('/rx/stop', methods=['PUT'])
def rx_find():
    pass


@sensors.route('/rx/found_devices', methods=['GET'])
def rx_find():
    pass