#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
import time
import threading
from rpi_rf import RFDevice


class RfDeviceHandler:
    def __init__(self):
        self.rfdevice = RFDevice(17)
        self.rfdevice.enable_tx()
        self.async_receive()

    def send(self):
        self.rfdevice.tx_code()

    def listening(self):
        timestamp = None
        while True:
            if self.rfdevice.rx_code_timestamp != timestamp:
                timestamp = self.rfdevice.rx_code_timestamp
                rx_code = self.rfdevice.rx_code
                rx_pulselength = self.rfdevice.rx_pulselength
                rx_proto = self.rfdevice.rx_proto
                logging.info("Signal detected: " + str(rx_code) + " [pulselength " + str(rx_pulselength) + ", protocol " + str(rx_proto) + "]")
            time.sleep(0.01)

    def async_receive(self):
        threading.Thread(target=self.listening).start()

    def destroy(self):
        self.rfdevice.cleanup()