#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
from datetime import datetime
from .dht_rpi import DHT22, ThermometerEntry
from ..gpio import RaspberryPi3 as GPIO_PI
from app.core.scheduler import scheduler, SchedulerTask
from app.database import db
from app.database.models import DataSource, DataSourceType
from app.database.converter import converter

_LOGGER = logging.getLogger(__name__)


class ThermometerDatabase(object):
    def __init__(self):
        self.db = db

    def save(self, dht_result: ThermometerEntry):
        return self.db.add_event(dht_result, DataSource.THERMOMETER, DataSourceType.SENSOR)

    def get_since(self, since: datetime):
        result_events = self.db.get_events_by(DataSource.THERMOMETER, DataSourceType.SENSOR, since)
        result = []
        for event in result_events:
            result.append(converter.structure(event.data, ThermometerEntry))
        return result

    def get_last(self):
        event = self.db.get_last_event(DataSource.THERMOMETER, DataSourceType.SENSOR)
        return converter.structure(event.data, ThermometerEntry)


class ThermometerController(object):
    def __init__(self):
        self.db = ThermometerDatabase()
        self.dht = DHT22(pin=GPIO_PI.GPIO_22.value)

        scheduler.register_task(SchedulerTask(name='thermometer', interval=60.0, delay=10.0,
                                              function=lambda: self.read()))

    def get_last(self):
        return self.db.get_last()

    def get_since(self, since: datetime):
        return self.db.get_since(since)

    def read(self):
        result = self.dht.get_result()
        if not(result is None):
            _LOGGER.info("Thermometer: %s", str(result))
            self.db.save(result)


thermometer_controller = ThermometerController()
