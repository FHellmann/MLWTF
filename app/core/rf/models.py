#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from datetime import datetime
from enum import Enum, unique

from attr import s, ib
from attr.validators import instance_of


@s(frozen=True)
class Protocol(object):
    pulse_length = ib(validator=instance_of(int))
    sync_high = ib(validator=instance_of(int))
    sync_low = ib(validator=instance_of(int))
    zero_high = ib(validator=instance_of(int))
    zero_low = ib(validator=instance_of(int))
    one_high = ib(validator=instance_of(int))
    one_low = ib(validator=instance_of(int))


@unique
class ProtocolType(Enum):
    PL_350 = Protocol(350, 1, 31, 1, 3, 3, 1)
    PL_650 = Protocol(650, 1, 10, 1, 2, 2, 1)
    PL_100 = Protocol(100, 30, 71, 4, 11, 9, 6)
    PL_380 = Protocol(380, 1, 6, 1, 3, 3, 1)
    PL_500 = Protocol(500, 6, 14, 1, 2, 2, 1)


@s(frozen=True)
class Signal(object):
    time = ib(validator=instance_of(datetime))
    code = ib(validator=instance_of(int))
    pulse_length = ib(validator=instance_of(int))
    bit_length = ib(validator=instance_of(int))
    protocol = ib(validator=instance_of(Protocol))
