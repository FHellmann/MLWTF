#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import threading
import time

from .rf_rpi import RFDevice
from .rf_signal import RfSignal


class RfController:
    def __init__(self):
        self.rf_sender = RFDevice(17, tx_proto=2)
        self.rf_sender.enable_tx()
        self.rf_receiver = RFDevice(27, tx_proto=2)
        self.rf_receiver.enable_rx()
        self.rf_signal_dict = {}
        threading.Thread(target=self.__listening).start()

    def __del__(self):
        self.rf_sender.cleanup()
        self.rf_receiver.cleanup()

    def send(self, rf_signal_key):
        rf_signal = self.rf_signal_dict[rf_signal_key]
        self.rf_sender.tx_code(rf_signal.get_code(), rf_signal.get_protocol(), rf_signal.get_pulselength())

    def get_signals(self):
        return self.rf_signal_dict.keys()

    def __listening(self):
        timestamp = None
        while True:
            if self.rf_receiver.rx_code_timestamp != timestamp:
                timestamp = self.rf_receiver.rx_code_timestamp
                rx_code = self.rf_receiver.rx_code
                rx_pulselength = self.rf_receiver.rx_pulselength
                rx_proto = self.rf_receiver.rx_proto

                rf_signal = RfSignal(timestamp, rx_code, rx_pulselength, rx_proto)
                self.rf_signal_dict[str(rf_signal.get_code())] = rf_signal

            time.sleep(0.01)
