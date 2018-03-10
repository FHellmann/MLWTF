#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
import threading
import time

from datetime import datetime
from .rf_rpi import Device
from ..gpio import RaspberryPi3 as GPIO_PI

_LOGGER = logging.getLogger(__name__)


class RxService:
    def __init__(self):
        self.rx_device = Device(GPIO_PI.GPIO_27.value)
        self.signal_list = []
        threading.Thread(target=self._listening).start()

    def __del__(self):
        self.rx_device.cleanup()

    def get_results(self, since):
        result = []

        for signal in self.signal_list:
            timestamp = (signal.time-datetime(1970,1,1)).total_seconds()
            _LOGGER.debug("Signal-Time=" + str(timestamp) + " <==> Since=" + str(since))
            if timestamp >= since:
                result.append(signal)

        return result

    def _listening(self):
        _LOGGER.debug("Listening for radio frequency signals")

        self.rx_device.enable_rx()

        timestamp = None
        while True:
            rf_signal = self.rx_device.rx_signal
            if not (rf_signal is None) and rf_signal.time != timestamp:
                timestamp = rf_signal.time

                self.signal_list.append(rf_signal)

                # To prevent a memory leak -> remove all cached entries older then 15 minutes
                cache_time_limit = 15 * 60
                while not self.signal_list and \
                        (datetime.utcnow() - self.signal_list[0].time).total_seconds() < cache_time_limit:
                    _LOGGER.debug("Pop signal with age '" +
                                  str((datetime.utcnow() - self.signal_list[0].time).total_seconds()) + "' seconds")
                    self.signal_list.pop(0)

            time.sleep(0.01)
