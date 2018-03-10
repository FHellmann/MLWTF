#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import request
from flask_restplus import Namespace, fields, Resource, reqparse
from marshmallow import Schema, fields as ma_fields, post_load, pprint

from app.database import session, RfSignal
from app.core.rf import send as rf_send

ns_rf = Namespace('rf', description='The radio frequency interface')

get_parser = reqparse.RequestParser()
get_parser.add_argument('since', type=int)

signal_model = ns_rf.model('Signal', {
    'time': fields.DateTime(readOnly=True, description='The time when the signal was received'),
    'code': fields.Integer(readOnly=True, description='The code of the received signal'),
    'pulse_length': fields.Integer(readOnly=True, description='The pulse length the signal was received over'),
    'bit_length': fields.Integer(readOnly=True, description='The bit length of the received signal'),
    'sync_high': fields.Integer(readOnly=True, description='The sync high of this protocol'),
    'sync_low': fields.Integer(readOnly=True, description='The sync low of this protocol'),
    'zero_high': fields.Integer(readOnly=True, description='The zero high of this protocol'),
    'zero_low': fields.Integer(readOnly=True, description='The zero low of this protocol'),
    'one_high': fields.Integer(readOnly=True, description='The one high of this protocol'),
    'one_low': fields.Integer(readOnly=True, description='The one low of this protocol')
})


class SignalSchema(Schema):
    time = ma_fields.DateTime()
    code = ma_fields.Integer()
    pulse_length = ma_fields.Integer()
    bit_length = ma_fields.Integer()
    sync_high = ma_fields.Integer()
    sync_low = ma_fields.Integer()
    zero_high = ma_fields.Integer()
    zero_low = ma_fields.Integer()
    one_high = ma_fields.Integer()
    one_low = ma_fields.Integer()

    @post_load
    def create_signal(self, data):
        return RfSignal(**data)


@ns_rf.route('/signals')
class SignalResource(Resource):

    @ns_rf.param('since', 'The time since when the signals should be fetched')
    def get(self):
        schema = SignalSchema(many=True)
        args = get_parser.parse_args()
        since = args['since']
        result = session.query(RfSignal).filter(RfSignal.time >= since).all()
        return schema.dump(result)

    @ns_rf.expect(signal_model, validate=True)
    @ns_rf.response(201, 'Signal send successful')
    @ns_rf.response(500, 'Failed to send signal')
    def post(self):
        schema = SignalSchema()
        signal = schema.load(request.json)
        pprint(signal)
        if rf_send(signal):
            return None, 201
        return None, 500
