#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>

    This is a layer between the raw execution unit and the database.
"""

import logging

from datetime import datetime

from . import rf_rpi
from .models import Protocol, Signal
from ..gpio import RaspberryPi3 as GPIO_PI
from app.database import db
from app.database.models import EventType, DataSourceType
from app.database.converter import converter

_LOGGER = logging.getLogger(__name__)


class RfDatabase(object):
    def __init__(self):
        self.db = db

    def save_received(self, signal : Signal):
        return self.db.add_event(converter.unstructure(signal), EventType.RADIO_FREQUENCY, DataSourceType.SENSOR)

    def save_send(self, signal : Signal):
        return self.db.add_event(converter.unstructure(signal), EventType.RADIO_FREQUENCY, DataSourceType.ACTUATOR)

    def get_received_signals_since(self, since : datetime):
        result_events = self.db.get_events_by(EventType.RADIO_FREQUENCY, DataSourceType.SENSOR, since)
        result = []
        for event in result_events:
            result.append(converter.structure(event.data, Signal))
        return result


class RfController(object):
    def __init__(self):
        self._db = RfDatabase()

        self._tx_device = rf_rpi.Device(GPIO_PI.GPIO_17.value)
        self._tx_device.enable_tx()

        self._rx_device = rf_rpi.Device(GPIO_PI.GPIO_27.value)
        self._rx_device.enable_rx()
        self._rx_device.add_rx_listener(self._receive)

    def __del__(self):
        self._tx_device.cleanup()
        self._rx_device.cleanup()

    def get_received_signals_since(self, since : datetime):
        return self._db.get_received_signals_since(since)

    def send(self, signal : Signal):
        _LOGGER.info("Sending radiofrequency signal: " + str(signal))
        success = self._tx_device.tx_code(signal)
        self._db.save_send(signal)
        return success

    def _receive(self, signal : Signal):
        _LOGGER.info("Receiving radiofrequency signal: " + str(signal))
        self._db.save_received(signal)

rf_controller = RfController()
