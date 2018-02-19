#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import json
from cattr import structure, unstructure

from flask import Blueprint

from .rx_service import RxService

sensors = Blueprint('sensors', __name__)

response_200 = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

rx_service = RxService()


@sensors.route('/', methods=['GET'])
def index():
    return response_200


@sensors.route('/rx/search', methods=['POST'])
def rx_find():
    rx_service.search_verified_signals(15)
    return response_200


@sensors.route('/rx/found_devices', methods=['GET'])
def get_rx_found_devices():
    return unstructure(rx_service.get_result())
