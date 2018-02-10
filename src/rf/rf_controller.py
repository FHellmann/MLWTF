#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
import threading
import time

from rpi_rf import RFDevice
from rf_signal import RfSignal


class RfController:
    def __init__(self):
        self.rfdevice = RFDevice(17)
        self.rfdevice.enable_tx()
        self.subscribers = []
        threading.Thread(target=self.listening).start()

    def __del__(self):
        self.rfdevice.cleanup()

    def send(self, rf_signal):
        self.rfdevice.send(rf_signal.get_code(), rf_signal.get_protocol(), rf_signal.get_pulselength())

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def listening(self):
        timestamp = None
        while True:
            if self.rfdevice.rx_code_timestamp != timestamp:
                timestamp = self.rfdevice.rx_code_timestamp
                rx_code = self.rfdevice.rx_code
                rx_pulselength = self.rfdevice.rx_pulselength
                rx_proto = self.rfdevice.rx_proto

                logging.info("Signal detected: " + str(rx_code) + " [pulselength " + str(rx_pulselength) + ", protocol " + str(rx_proto) + "]")
                for subscriber in self.subscribers:
                    subscriber(RfSignal(timestamp, rx_code, rx_pulselength, rx_proto))

            time.sleep(0.01)
