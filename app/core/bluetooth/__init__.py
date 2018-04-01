#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from .models import BluetoothDevice
from .bt_rpi import BluetoothConnector, BluetoothDevice


class BluetoothController(object):
    def __init__(self):
        self.btle_rpi = BluetoothConnector()

    def scan(self):
        return self.btle_rpi.scan()

    def connect(self, device: BluetoothDevice):
        self.btle_rpi.connect(device)

    def write(self, value):
        self.btle_rpi.send(value)


bt_controller = BluetoothController()
