#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import request
from flask_restplus import Namespace, fields, Resource, reqparse
from marshmallow import Schema, fields as ma_fields, post_load

from datetime import datetime

from app.core.rf import rf_controller, Signal, Protocol

ns_rf = Namespace('rf', description='The radio frequency interface')

get_parser = reqparse.RequestParser()
get_parser.add_argument('since', type=int)

protocol_model = ns_rf.model('Protocol', {
    'pulselength': fields.Integer(readOnly=True, description='The pulse length of this protocol'),
    'sync_high': fields.Integer(readOnly=True, description='The sync high of this protocol'),
    'sync_low': fields.Integer(readOnly=True, description='The sync low of this protocol'),
    'zero_high': fields.Integer(readOnly=True, description='The zero high of this protocol'),
    'zero_low': fields.Integer(readOnly=True, description='The zero low of this protocol'),
    'one_high': fields.Integer(readOnly=True, description='The one high of this protocol'),
    'one_low': fields.Integer(readOnly=True, description='The one low of this protocol')
})

signal_model = ns_rf.model('Signal', {
    'time': fields.DateTime(readOnly=True, description='The time when the signal was received'),
    'code': fields.Integer(readOnly=True, description='The code of the received signal'),
    'pulselength': fields.Integer(readOnly=True, description='The pulse length the signal was received over'),
    'bit_length': fields.Integer(readOnly=True, description='The bit length of the received signal'),
    'protocol': fields.Nested(protocol_model, skipNone=False, allow_null=False, readOnly=True,
                              description='The protocol of the received signal')
})


class ProtocolSchema(Schema):
    pulse_length = ma_fields.Integer()
    sync_high = ma_fields.Integer()
    sync_low = ma_fields.Integer()
    zero_high = ma_fields.Integer()
    zero_low = ma_fields.Integer()
    one_high = ma_fields.Integer()
    one_low = ma_fields.Integer()

    @post_load
    def create_protocol(self, data):
        return Protocol(**data)


class SignalSchema(Schema):
    time = ma_fields.DateTime()
    code = ma_fields.Integer()
    pulse_length = ma_fields.Integer()
    bit_length = ma_fields.Integer()
    protocol = ma_fields.Nested(ProtocolSchema())

    @post_load
    def create_signal(self, data):
        return Signal(**data)


@ns_rf.route('/signals')
class SignalResource(Resource):

    @ns_rf.param('since', 'The time since when the signals should be fetched')
    def get(self):
        schema = SignalSchema(many=True)
        args = get_parser.parse_args()
        since = datetime.fromtimestamp(args['since'])
        result = rf_controller.get_received_signals_since(since)
        return schema.dump(result)

    @ns_rf.expect(signal_model, validate=True)
    @ns_rf.response(201, 'Signal send successful')
    @ns_rf.response(500, 'Failed to send signal')
    def post(self):
        schema = SignalSchema()
        signal = schema.load(request.json)
        if rf_controller.send(signal):
            return None, 201
        return None, 500
