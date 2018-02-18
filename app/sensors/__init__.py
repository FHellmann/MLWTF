#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Blueprint, request, abort, jsonify
import json
from .rx_service import RxService

sensors = Blueprint('sensors', __name__)

rx_service = RxService()


@sensors.route('/', methods=['GET'])
def index():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@sensors.route('/rx/search', methods=['PUT'])
def rx_find():
    rx_service.search_verified_signals(30)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@sensors.route('/rx/found_devices', methods=['GET'])
def get_rx_found_devices():
    return jsonify(rx_service.get_result())
