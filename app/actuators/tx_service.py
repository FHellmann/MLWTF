#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from ..hardware.rf_rpi import Device
from ..hardware.gpio import RaspberryPi3 as GPIO_PI


class TxService:
    def __init__(self):
        self.tx_device = Device(GPIO_PI.GPIO_17.value)
        self.tx_device.enable_rx()

    def __del__(self):
        self.tx_device.cleanup()

    def send(self, signal):
        return self.tx_device.tx_code(signal)
