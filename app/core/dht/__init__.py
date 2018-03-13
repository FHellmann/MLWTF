#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from app.core.gpio import RaspberryPi3
from .dht22 import DHT22, DHT22Result

dht = DHT22(pin=RaspberryPi3.GPIO_14_TXD)