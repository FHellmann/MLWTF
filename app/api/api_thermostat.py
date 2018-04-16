#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask_restplus import Namespace, Resource, reqparse
from marshmallow import Schema, fields as ma_fields, post_load

from app.core.bluetooth import bt_controller, BLEDevice

ns_ts = Namespace('thermostat', description='The thermostat interface')

get_parser = reqparse.RequestParser()
get_parser.add_argument('since', type=int)


class BTDeviceSchema(Schema):
    mac = ma_fields.String()

    @post_load
    def create_bt_device(self, data):
        return BLEDevice(**data)


@ns_ts.route('/all')
class BluetoothDeviceCollectionResource(Resource):

    def get(self):
        schema = BTDeviceSchema(many=True)
        result = bt_controller.scan()
        return schema.dump(result)
