#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import json
from cattr import structure, unstructure
from flask import Blueprint
from .rx_service import RxService

sensors = Blueprint('sensors', __name__)
rx_service = RxService()


@sensors.route('/', methods=['GET'])
def index():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@sensors.route('/rx/signals/search', methods=['POST'])
def rx_find():
    success = rx_service.search_verified_signals(15)
    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}


@sensors.route('/rx/signals', methods=['GET'])
def get_rx_found_devices():
    return unstructure(rx_service.get_result())
