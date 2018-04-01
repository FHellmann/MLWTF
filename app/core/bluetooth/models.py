#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from attr import s, ib
from attr.validators import instance_of


@s(frozen=True)
class BluetoothDevice(object):
    mac = ib(validator=instance_of(str), type=str)
