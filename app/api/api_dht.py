#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask_restplus import Namespace, Resource, reqparse
from marshmallow import Schema, fields as ma_fields, post_load

from datetime import datetime

from app.core.dht import dht_controller, DHTResult, DHTErrorCode

ns_dht = Namespace('dht', description='The humidity temperature interface')

get_parser = reqparse.RequestParser()
get_parser.add_argument('since', type=int)


class DHTResultSchema(Schema):
    humidity = ma_fields.Float()
    temperature = ma_fields.Float()
    timestamp = ma_fields.DateTime()

    @post_load
    def create_dht_result(self, data):
        return DHTResult(**data)


@ns_dht.route('/all')
class DhtCollectionResource(Resource):

    @ns_dht.param('since', 'The time since when the signals should be fetched')
    def get(self):
        schema = DHTResultSchema(many=True)
        args = get_parser.parse_args()
        since = datetime.fromtimestamp(args['since'])
        result = dht_controller.get_since(since)
        return schema.dump(result)


@ns_dht.route('/last')
class DhtResource(Resource):

    def get(self):
        schema = DHTResultSchema()
        result = dht_controller.get_last()
        return schema.dump(result)
