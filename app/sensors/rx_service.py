#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import threading
import time
import logging
from datetime import datetime

from ..hardware.rf_rpi import Device
from ..hardware.gpio import RaspberryPi3 as GPIO_PI

_LOGGER = logging.getLogger(__name__)


class RxService:
    def __init__(self):
        self.rx_device = Device(GPIO_PI.GPIO_27.value)
        self.result = None

    def __del__(self):
        self.rx_device.cleanup()

    def search_verified_signals(self, time_to_search_sec):
        _LOGGER.debug("Start search for verified signals")
        threading.Thread(target=self._listening, args=(time_to_search_sec,)).start()

    def get_result(self):
        return self.result

    def _listening(self, time_to_search_sec):
        self.rx_device.enable_rx()
        rf_signal_counter = {}
        rf_signal_dict = {}
        self.result = []
        start_time = datetime.now()

        timestamp = None
        while (datetime.now() - start_time).seconds < time_to_search_sec:
            if not(self.rx_device.rx_signal is None) and self.rx_device.rx_signal.time != timestamp:
                rf_signal = self.rx_device.rx_signal
                timestamp = rf_signal.time

                rf_signal_dict[str(rf_signal.code)] = rf_signal
                rf_signal_counter[str(rf_signal.code)] += 1

                # Signal found -> filter only the signals we would like to see
                if rf_signal_counter[str(rf_signal.code)] >= 3:
                    _LOGGER.debug("Found verified signal: " + str(rf_signal))
                    self.result.append(rf_signal)

            time.sleep(0.01)

        self.rx_device.disable_rx()
        _LOGGER.debug("Finish search for verified signals")