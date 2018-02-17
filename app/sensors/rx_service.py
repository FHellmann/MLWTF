#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import threading
import time
import logging

from ..hardware.rf_rpi import Device
from ..hardware.gpio import RaspberryPi3 as GPIO_PI

_LOGGER = logging.getLogger(__name__)


class RxService:
    def __init__(self):
        self.rx_device = Device(GPIO_PI.GPIO_27)

    def __del__(self):
        self.rx_device.cleanup()

    def find_verified_signals(self, time_to_search_sec, callback):
        threading.Thread(target=self._listening, args={time_to_search_sec, callback}).start()

    def _listening(self, time_to_search_sec, callback):
        self.rx_device.enable_rx()
        search_verified_signals = True
        search_verified_signals_timer = time.time()
        rf_signal_counter = {}
        rf_verified_signal = None
        rf_signal_dict = {}

        timestamp = None
        while True:
            if search_verified_signals and self.rx_device.rx_signal.time != timestamp:
                rf_signal = self.rx_device.rx_signal
                timestamp = rf_signal.time

                rf_signal_dict[str(rf_signal.code)] = rf_signal
                rf_signal_counter[str(rf_signal.code)] += 1

                # Signal found -> filter only the signals we would like to see
                if rf_signal_counter[str(rf_signal.code)] >= 3:
                    rf_verified_signal = rf_signal
                    search_verified_signals = False

            time.sleep(0.01)

        self.rx_device.disable_rx()