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
class EventType(Enum):
    """
    The event type describes the type of data which is hold inside the data block
    """
    RADIO_FREQUENCY = 'radio_frequency'
    HUMIDITY_TEMPERATURE = 'humidity_temperature'


@s(frozen=True)
class Event(object):
    """
    The event is a global container for every incoming and outgoing signal
    """
    data = ib()
    event_type = ib(validator=instance_of(EventType), type=EventType)
    data_source_type = ib(validator=instance_of(DataSourceType), type=DataSourceType)
    timestamp = ib(validator=instance_of(datetime), type=datetime, default=datetime.utcnow())


@s(frozen=True)
class NamedEvent(object):
    """
    The named event will be used from devices to recognize events by their names
    """
    name = ib(validator=instance_of(str), type=str)
    event = ib(validator=instance_of(Event), type=Event)


@s(frozen=True)
class Device(object):
    """
    Every controllable device
    """
    data = ib()
    name = ib(validator=instance_of(str), type=str)
    location = ib(validator=instance_of(str), type=str)
    description = ib(validator=instance_of(str), type=str, default='')
