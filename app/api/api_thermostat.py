#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask_restplus import Namespace, Resource, reqparse
from marshmallow import Schema, fields as ma_fields, post_load

from app.core.thermostat import thermostat_controller, Thermostat, ThermostatManufacturer

ns_ts = Namespace('thermostat', description='The thermostat interface')

get_parser = reqparse.RequestParser()
get_parser.add_argument('since', type=int)


class ThermostatManufacturerSchema(Schema):
    name = ma_fields.String()

    @post_load
    def create_protocol(self, data):
        return ThermostatManufacturer(**data)

class ThermostatSchema(Schema):
    addr = ma_fields.String()
    name = ma_fields.String()
    issr = ma_fields.String()
    manufacturer = ma_fields.Nested(ThermostatManufacturerSchema())

    @post_load
    def create(self, data):
        return Thermostat(**data)


@ns_ts.route('/all')
class ThermostatCollectionResource(Resource):

    def get(self):
        schema = ThermostatSchema(many=True)
        result = thermostat_controller.scan()
        return schema.dump(result)
