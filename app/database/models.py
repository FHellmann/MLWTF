#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from datetime import datetime
from enum import Enum, unique

from attr import s, ib
from attr.validators import instance_of


@unique
class DataSourceType(Enum):
    """
    The data source type describes the origin of the data
    """
    SENSOR = 'sensor'
    ACTUATOR = 'actuator'


@unique
class DataSource(Enum):
    """
    The event type describes the type of data which is hold inside the data block
    """
    LOW_RADIO_FREQUENCY = 'radio_frequency_433Mhz'
    THERMOMETER = 'thermometer'
    THERMOSTAT = 'thermostat'


@s(frozen=True)
class User(object):
    """
    The user who triggered an event
    """
    name = ib(validator=instance_of(str), type=str, default='System')


@s(frozen=True)
class Event(object):
    """
    The event is a global container for every incoming and outgoing signal
    """
    data = ib()
    data_source = ib(validator=instance_of(DataSource), type=DataSource)
    data_source_type = ib(validator=instance_of(DataSourceType), type=DataSourceType)
    timestamp = ib(validator=instance_of(datetime), type=datetime, default=datetime.utcnow())
    user = ib(validator=instance_of(User), type=User, default=User())


@s(frozen=True)
class Device(object):
    """
    Every controllable device
    """
    data = ib()
    name = ib(validator=instance_of(str), type=str)
    description = ib(validator=instance_of(str), type=str, default='')
