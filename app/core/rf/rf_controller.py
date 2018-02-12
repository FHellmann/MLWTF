#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import threading
import time
import datetime

from .rf_rpi import RFDevice
from .rf_signal import RfSignal


class RfController:
    def __init__(self):
        self.rf_sender = RFDevice(17, tx_proto=2)
        self.rf_sender.enable_tx()
        self.rf_receiver = RFDevice(27, tx_proto=2)
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
        return self.rf_sender.tx_code(rf_signal.get_code(), rf_signal.get_protocol(), rf_signal.get_pulselength())

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
            if self.search_verified_signals and self.rf_receiver.rx_code_timestamp != timestamp:
                timestamp = self.rf_receiver.rx_code_timestamp
                rx_code = self.rf_receiver.rx_code
                rx_pulselength = self.rf_receiver.rx_pulselength
                rx_proto = self.rf_receiver.rx_proto

                rf_signal = RfSignal(timestamp, rx_code, rx_pulselength, rx_proto)
                self.rf_signal_dict[str(rf_signal.get_code())] = rf_signal
                self.rf_signal_counter[str(rf_signal.get_code())] += 1

                # Signal found -> filter only the signals we would like to see
                if self.rf_signal_counter[str(rf_signal.get_code())] >= 3:
                    self.rf_verified_signal = rf_signal
                    self.search_verified_signals = False

            time.sleep(0.01)
