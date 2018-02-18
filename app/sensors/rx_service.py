#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
import threading
import time
from datetime import datetime

from ..hardware.gpio import RaspberryPi3 as GPIO_PI
from ..hardware.rf_rpi import Device

_LOGGER = logging.getLogger(__name__)


class RxService:
    def __init__(self):
        self.rx_device = Device(GPIO_PI.GPIO_27.value)
        self.result = None
        self.searching = False

    def __del__(self):
        self.rx_device.cleanup()

    def search_verified_signals(self, time_to_search_sec):
        if self.searching:
            return
        threading.Thread(target=self._listening, args=(time_to_search_sec,)).start()

    def get_result(self):
        return self.result

    def _listening(self, time_to_search_sec):
        _LOGGER.debug("Start search for verified signals")

        self.searching = True
        self.rx_device.enable_rx()
        rf_signal_codes = {}
        self.result = []
        start_time = datetime.now()

        timestamp = None
        while (datetime.now() - start_time).seconds < time_to_search_sec:
            rf_signal = self.rx_device.rx_signal
            if not (rf_signal is None) and rf_signal.time != timestamp:
                timestamp = rf_signal.time

                if rf_signal.code not in rf_signal_codes:
                    rf_signal_codes[rf_signal.code] = 1
                rf_signal_codes[rf_signal.code] += 1

                # Signal found -> filter only the signals we would like to see
                if rf_signal_codes[rf_signal.code] >= 3:
                    _LOGGER.debug("Found verified signal: " + str(rf_signal))
                    self.result.append(rf_signal)

            time.sleep(0.01)

        self.rx_device.disable_rx()
        self.searching = False

        _LOGGER.debug("Finish search for verified signals (Found=" + str(len(self.result)) + ")")
