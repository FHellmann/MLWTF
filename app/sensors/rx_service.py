#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import threading
import time
import datetime

from ..hardware.rf_rpi import Device
from ..hardware.gpio import RaspberryPi3 as GPIO_PI


class RfController:
    def __init__(self):
        self.rf_sender = Device(GPIO_PI.GPIO_17)
        self.rf_sender.enable_tx()
        self.rf_receiver = Device(GPIO_PI.GPIO_27)
        self.rf_receiver.enable_rx()
        self.search_verified_signals = False
        self.search_verified_signals_timer = None
        self.rf_signal_counter = {}
        self.rf_verified_signal = None
        self.rf_signal_dict = {}
        threading.Thread(target=self.__listening).start()

    def __del__(self):
        self.rf_sender.cleanup()
        self.rf_receiver.cleanup()

    def send(self, rf_signal_key):
        rf_signal = self.rf_signal_dict[rf_signal_key]
        return self.rf_sender.tx_code(rf_signal)

    def get_signals(self):
        return self.rf_signal_dict.keys()

    def get_verified_signal(self):
        return self.rf_verified_signal

    def search_for_verified_signals(self, time_to_search_sec):
        self.search_verified_signals = True
        self.search_verified_signals_timer = time.time()
        self.rf_signal_counter = {}
        self.rf_verified_signal = None
        self.rf_signal_dict = {}

    def __listening(self):
        timestamp = None
        while True:
            if self.search_verified_signals and self.rf_receiver.rx_signal.time != timestamp:
                rf_signal = self.rf_receiver.rx_signal
                timestamp = rf_signal.time

                self.rf_signal_dict[str(rf_signal.code)] = rf_signal
                self.rf_signal_counter[str(rf_signal.code)] += 1

                # Signal found -> filter only the signals we would like to see
                if self.rf_signal_counter[str(rf_signal.code)] >= 3:
                    self.rf_verified_signal = rf_signal
                    self.search_verified_signals = False

            time.sleep(0.01)