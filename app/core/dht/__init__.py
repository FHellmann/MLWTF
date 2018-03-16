#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
from datetime import datetime
from .dht_rpi import DHT22, DHTResult, DHTErrorCode
from ..gpio import RaspberryPi3 as GPIO_PI
from app.core.scheduler import scheduler, SchedulerTask
from app.database import db
from app.database.models import EventType, DataSourceType
from app.database.converter import converter

_LOGGER = logging.getLogger(__name__)


class DhtDatabase(object):
    def __init__(self):
        self.db = db
        converter.register_structure_hook(DHTErrorCode, lambda error_code_name, cls: DHTErrorCode(error_code_name))

    def save(self, dht_result: DHTResult):
        return self.db.add_event(dht_result, EventType.HUMIDITY_TEMPERATURE, DataSourceType.SENSOR)

    def get_since(self, since: datetime):
        result_events = self.db.get_events_by(EventType.HUMIDITY_TEMPERATURE, DataSourceType.SENSOR, since)
        result = []
        for event in result_events:
            result.append(converter.structure(event.data, DHTResult))
        return result

    def get_last(self):
        event = self.db.get_last_event(EventType.HUMIDITY_TEMPERATURE, DataSourceType.SENSOR)
        return converter.structure(event.data, DHTResult)


class DhtController(object):
    def __init__(self):
        self.db = DhtDatabase()
        self.dht = DHT22(pin=GPIO_PI.GPIO_22.value)

        scheduler.register_task(SchedulerTask(name='dht', interval=60.0, delay=10.0, function=lambda: self.read()))

    def get_last(self):
        return self.db.get_last()

    def get_since(self, since: datetime):
        return self.db.get_since(since)

    def read(self):
        error, result = self.dht.get_result_once()
        _LOGGER.info("Error: " + str(error) + ", Result: " + str(result))
        if error == DHTErrorCode.ERR_NO_ERROR:
            self.db.save(result)


dht_controller = DhtController()
