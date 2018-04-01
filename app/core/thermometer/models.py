#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from attr import s, ib
from attr.validators import instance_of
from datetime import datetime


@s(frozen=True)
class ThermometerEntry:
    """"
    DHT sensor result returned by DHT.read() method
    """
    timestamp = ib(validator=instance_of(datetime), type=datetime)
    temperature = ib(validator=instance_of(float), type=float)
    humidity = ib(validator=instance_of(float), type=float)
