#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from . import sensors
from flask import request, abort, jsonify
from .rx_service import RxService

# Define services
rx_service = RxService()

# Define Rest Calls


@sensors.route('/', methods=['GET'])
def index():
    pass


@sensors.route('/rx/search', methods=['PUT'])
def rx_find():
    rx_service.search_verified_signals(30)


@sensors.route('/rx/found_devices', methods=['GET'])
def rx_find():
    return jsonify(rx_service.get_result())
