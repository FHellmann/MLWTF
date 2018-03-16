#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from attr import s, ib
from attr.validators import instance_of
from enum import Enum, unique
from datetime import datetime


@unique
class DHTErrorCode(Enum):
    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CHECKSUM = 2


@s(frozen=True)
class DHTResult:
    """"
    DHT sensor result returned by DHT.read() method
    """
    timestamp = ib(validator=instance_of(datetime), type=datetime)
    temperature = ib(validator=instance_of(float), type=float, default=-1.0)
    humidity = ib(validator=instance_of(float), type=float, default=-1.0)
