"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>

    Sending and receiving 433/315Mhz signals with low-cost GPIO RF Modules on a Raspberry Pi.

    Original: https://github.com/milaq/rpi-rf
"""

from enum import Enum, unique
from datetime import datetime
import attr
from attr.validators import instance_of


@attr.s(frozen=True)
class Protocol(object):
    pulselength = attr.ib(validator=instance_of(int))
    sync_high = attr.ib(validator=instance_of(int))
    sync_low = attr.ib(validator=instance_of(int))
    zero_high = attr.ib(validator=instance_of(int))
    zero_low = attr.ib(validator=instance_of(int))
    one_high = attr.ib(validator=instance_of(int))
    one_low = attr.ib(validator=instance_of(int))


@unique
class ProtocolType(Enum):
    PL_350 = Protocol(350, 1, 31, 1, 3, 3, 1)
    PL_650 = Protocol(650, 1, 10, 1, 2, 2, 1)
    PL_100 = Protocol(100, 30, 71, 4, 11, 9, 6)
    PL_380 = Protocol(380, 1, 6, 1, 3, 3, 1)
    PL_500 = Protocol(500, 6, 14, 1, 2, 2, 1)


@attr.s(frozen=True)
class Signal(object):
    time = attr.ib(validator=instance_of(datetime))
    code = attr.ib(validator=instance_of(int))
    pulselength = attr.ib(validator=instance_of(int))
    bit_length = attr.ib(validator=instance_of(int))
    protocol = attr.ib(validator=instance_of(ProtocolType))


@attr.s(frozen=True)
class SignalCollection(object):
    signals = attr.ib()
