#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from attr import s, ib
from attr.validators import instance_of


@s(frozen=True)
class BLEDevice(object):
    """
    Device MAC address (as a hex string separated by colons).
    """
    addr = ib(validator=instance_of(str), type=str)
    """
    The name which is set 
    """
    name = ib(validator=instance_of(str), type=str)
    """
    Received Signal Strength Indication for the last received broadcast from the device. This is an integer value 
    measured in dB, where 0 dB is the maximum (theoretical) signal strength, and more negative numbers indicate a 
    weaker signal.
    """
    rssi = ib(validator=instance_of(int), type=int)
