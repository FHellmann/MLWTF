#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>

    This is a layer between the raw execution unit and the database.
"""

import logging

from datetime import datetime
from typing import List

from . import rf_rpi
from .models import Protocol, Signal, SignalContainer
from ..gpio import RaspberryPi3 as GPIO_PI
from app.database import db, Query
from app.database.cattr_util import converter

_LOGGER = logging.getLogger(__name__)


class RfDatabase(object):
    def __init__(self):
        self.rf_table = db.get().table('rf_table')

    def save(self, signal : Signal, received : bool):
        signal_container = SignalContainer(signal=signal, received=received)
        signal_container_db = converter.unstructure(signal_container)
        self.rf_table.insert(signal_container_db)

    def get_received_signals_since(self, since : datetime):
        received_signals_db = self.rf_table.search(
            (Query().received == True) & (Query().signal.time >= since.timestamp())
        )
        search = converter.structure(received_signals_db, List[SignalContainer])

        result = []
        for signal_container in search:
            result.append(signal_container.signal)

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
        _LOGGER.info("Sending rf signal: " + str(signal))
        success = self._tx_device.tx_code(signal)
        self._db.save(Signal(datetime.utcnow(), signal.code, signal.pulse_length, signal.bit_length, signal.protocol),
                      False)
        return success

    def _receive(self, signal : Signal):
        _LOGGER.info("Receiving rf signal: " + str(signal))
        self._db.save(signal, True)

rf_controller = RfController()
