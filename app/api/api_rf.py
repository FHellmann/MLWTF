#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask_restplus import Resource

from . import api
from ..core.rf.rx_service import RxService
from ..core.rf.tx_service import TxService

rx_service = RxService()
tx_service = TxService()

api_rf = api.namespace('/rf', description='Test')


@api_rf.route('/signals')
class SignalItem(Resource):
    @api_rf.response(201, 'Signal send successful')
    def send(self, signal):
        if tx_service.send(signal):
            return None, 201
        return None, 500


@api_rf.route('/signals')
class SignalCollection(Resource):
    @api_rf.marshal_list_with(SignalItem)
    def get(self):
        rx_service.get_result()

    @api_rf.response(201, 'Signal send successful')
    def find(self):
        rx_service.search_verified_signals(15)
        return None, 201
