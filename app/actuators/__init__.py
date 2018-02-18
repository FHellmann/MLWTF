#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import json

from flask import Blueprint, request, abort

from .tx_service import TxService

actuators = Blueprint('actuators', __name__)

response_200 = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

tx_service = TxService()


@actuators.route('/', methods=['GET'])
def index():
    pass


@actuators.route('/tx/send', methods=['POST'])
def tx_send():
    if not request.json:
        abort(400)
    # TODO Convert request.json into rf_rpi.Signal
    # tx_service.send(signal)
