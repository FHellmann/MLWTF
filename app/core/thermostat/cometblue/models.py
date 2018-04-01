#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from attr import s, ib
from attr.validators import instance_of
from enum import Enum, unique
from datetime import datetime


@unique
class StructPacking(Enum):
    PIN = '<I'
    BATTERY = '<B'
    DATETIME = '<BBBBB'
    STATUS = '<BBB'
    TEMPERATURES = '<bbbbbbb'
    LCD_TIMER = '<BB'
    DAY = '<BBBBBBBB'
    HOLIDAY = '<BBBBBBBBb'


@s(frozen=True)
class Holiday(object):
    start = ib(validator=instance_of(datetime), type=datetime)
    end = ib(validator=instance_of(datetime), type=datetime)
    temperature = ib(validator=instance_of(float), type=float)

    def is_active(self):
        return not(self.start is None) and not(self.end is None) and not(self.temperature is None)


@s(frozen=True)
class Day(object):
    start = ib(validator=instance_of(datetime), type=datetime)
    end = ib(validator=instance_of(datetime), type=datetime)


@s(frozen=True)
class Status(object):
    state_as_dword = ib(validator=instance_of(str), type=str)
    unused_bits = ib(validator=instance_of(int), type=int)


@s(frozen=True)
class Temperature(object):
    current_temp = ib(validator=instance_of(float), type=float)
    manual_temp = ib(validator=instance_of(float), type=float)
    target_temp_l = ib(validator=instance_of(float), type=float)
    target_temp_h = ib(validator=instance_of(float), type=float)
    offset_temp = ib(validator=instance_of(float), type=float)
    window_open_detection = ib(validator=instance_of(int), type=int)
    window_open_minutes = ib(validator=instance_of(int), type=int)