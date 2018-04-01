#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask_restplus import Namespace, Resource, reqparse
from marshmallow import Schema, fields as ma_fields, post_load

from datetime import datetime

from app.core.thermometer import thermometer_controller, ThermometerEntry

ns_tm = Namespace('thermometer', description='The thermometer interface')

get_parser = reqparse.RequestParser()
get_parser.add_argument('since', type=int)


class ThermometerEntrySchema(Schema):
    humidity = ma_fields.Float()
    temperature = ma_fields.Float()
    timestamp = ma_fields.DateTime()

    @post_load
    def create_thermometer_entry(self, data):
        return ThermometerEntry(**data)


@ns_tm.route('/entry/all')
class ThermometerEntryCollectionResource(Resource):

    @ns_tm.param('since', 'The time since when the signals should be fetched')
    def get(self):
        schema = ThermometerEntrySchema(many=True)
        args = get_parser.parse_args()
        since_ = args['since']
        since = datetime.fromtimestamp(since_)
        result = thermometer_controller.get_since(since)
        return schema.dump(result)


@ns_tm.route('/entry/last')
class ThermometerEntryResource(Resource):

    def get(self):
        schema = ThermometerEntrySchema()
        result = thermometer_controller.get_last()
        return schema.dump(result)
