#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import json
from cattr import structure, unstructure
from flask import Blueprint, request, abort
from .tx_service import TxService
from ..hardware.rf_rpi import Signal

actuators = Blueprint('actuators', __name__)
tx_service = TxService()


@actuators.route('/', methods=['GET'])
def index():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@actuators.route('/tx/signal/send', methods=['POST'])
def tx_send():
    if not request.json:
        abort(400)
    signal = structure(request.data, Signal)
    success = tx_service.send(signal)
    return json.dumps({'success': success}), 200, {'ContentType': 'application/json'}
