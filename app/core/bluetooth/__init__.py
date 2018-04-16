#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from .models import BLEDevice
from .bt_rpi import BluetoothConnector


class BluetoothController(object):
    def __init__(self):
        self.btle_rpi = BluetoothConnector()

    def scan(self):
        return self.btle_rpi.scan()

    def connect(self, device: BLEDevice, callback_function):
        self.btle_rpi.connect(device, callback_function)

    def disconnect(self):
        self.btle_rpi.disconnect()

    def write(self, value):
        self.btle_rpi.send(value)


bt_controller = BluetoothController()
