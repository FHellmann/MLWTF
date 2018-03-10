#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import request
from flask_restplus import Namespace, Resource, reqparse
from marshmallow import Schema, fields, post_load

from ..core.rf import Signal, Protocol, tx_service, rx_service

ns_rf = Namespace('rf', description='The radio frequency interface')

get_parser = reqparse.RequestParser()
get_parser.add_argument('since', type=int)


class ProtocolSchema(Schema):
    pulse_length = fields.Integer()
    sync_high = fields.Integer()
    sync_low = fields.Integer()
    zero_high = fields.Integer()
    zero_low = fields.Integer()
    one_high = fields.Integer()
    one_low = fields.Integer()

    @post_load
    def create_protocol(self, data):
        return Protocol(**data)


class SignalSchema(Schema):
    time = fields.DateTime()
    code = fields.Integer()
    pulse_length = fields.Integer()
    bit_length = fields.Integer()
    protocol = fields.Nested(ProtocolSchema())

    @post_load
    def create_signal(self, data):
        return Signal(**data)


@ns_rf.route('/signals')
class SignalResource(Resource):

    @ns_rf.param('since', 'The time since when the signals should be fetched')
    def get(self):
        args = get_parser.parse_args()
        since = args['since']
        return rx_service.get_results(since)

    @ns_rf.response(201, 'Signal send successful')
    @ns_rf.response(500, 'Failed to send signal')
    def post(self):
        schema = SignalSchema()
        signal = schema.load(request.json).data
        if tx_service.send(signal):
            return None, 201
        return None, 500
