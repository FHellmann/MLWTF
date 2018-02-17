#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from . import actuators
from flask import request, abort
from .tx_service import TxService


# Define services
tx_service = TxService()


# Define Rest Calls

@actuators.route('/', methods=['GET'])
def index():
    pass


@actuators.route('/tx/send', methods=['POST'])
def tx_send():
    if not request.json:
        abort(400)
    # TODO Convert request.json into rf_rpi.Signal
    # tx_service.send(signal)
