#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
from datetime import datetime
from app.core.bluetooth import bt_controller
from app.core.thermostat.models import ThermostatEntry, ThermostatManufacturer, Thermostat
from app.database import db
from app.database.models import DataSource, DataSourceType
from app.database.converter import converter

_LOGGER = logging.getLogger(__name__)


class ThermostatDatabase(object):
    def __init__(self):
        self.db = db

    def save(self, dht_result: ThermostatEntry):
        return self.db.add_event(dht_result, DataSource.THERMOSTAT, DataSourceType.ACTUATOR)

    def get_since(self, since: datetime):
        result_events = self.db.get_events_by(DataSource.THERMOSTAT, DataSourceType.ACTUATOR, since)
        result = []
        for event in result_events:
            result.append(converter.structure(event.data, ThermostatEntry))
        return result

    def get_last(self):
        event = self.db.get_last_event(DataSource.THERMOSTAT, DataSourceType.ACTUATOR)
        return converter.structure(event.data, ThermostatEntry)


class ThermostatController(object):
    def __init__(self):
        self.db = ThermostatDatabase()
        self.bt = bt_controller

    def scan(self):
        devices = self.bt.scan()
        result = []
        # filter all devices which are not recognizable by the thermostat manufacturers
        for device in devices:
            for manufacturer in ThermostatManufacturer:
                if device.name.lower() == manufacturer.value.lower():
                    result.append(Thermostat(addr=device.addr,
                                             name=device.name,
                                             rssi=device.rssi,
                                             manufacturer=manufacturer
                                             ))
        return result

    def connect(self, device: Thermostat):
        self.bt.connect(device, self._callback_function)

    def disconnect(self):
        self.bt.disconnect()

    def get_since(self, since: datetime):
        return self.db.get_since(since)

    def _callback_function(self, value):
        _LOGGER.debug("Reading %s from device %s", value, self.bt.mac)


thermostat_controller = ThermostatController()
