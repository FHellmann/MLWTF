#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from typing import List
from datetime import datetime

from .models import Event, EventType, DataSourceType
from .converter import converter
from app.core.threading_utils import RWLock

_LOGGER = logging.getLogger(__name__)


class Database(object):
    class __Database(object):
        def __init__(self):
            # Default: use in-memory database
            self.db = TinyDB(storage=MemoryStorage)
            self.table_events = None
            self.table_users = None
            self.table_devices = None
            self.lock = RWLock()

        def __del__(self):
            self.db.close()

    instance = None

    def __init__(self):
        if not self.instance:
            self.instance = Database.__Database()
            self.setup(None)

    def setup(self, path):
        if not (path is None):
            self.instance.db = TinyDB(path)

        self.instance.table_events = self.instance.db.table('events')
        self.instance.table_users = self.instance.db.table('users')
        self.instance.table_devices = self.instance.db.table('devices')

    def add_event(self, data, event_type: EventType, data_source_type: DataSourceType):
        with self.instance.lock.writer():
            event = Event(event_type=event_type, data_source_type=data_source_type, data=data)
            unstructure = converter.unstructure(event)
            self.instance.table_events.insert(unstructure)
            return event

    def get_event(self, event_id: int):
        with self.instance.lock.reader():
            event = self.instance.table_events.get(doc_id=event_id)
            return event

    def get_events_by(self, event_type: EventType, data_source_type: DataSourceType,
                      since: datetime = datetime.utcnow()):
        with self.instance.lock.reader():
            search = self.instance.table_events.search(
                (Query().event_type == event_type.value) &
                (Query().data_source_type == data_source_type.value) &
                (Query().timestamp >= since.timestamp())
            )
            structure = converter.structure(search, List[Event])
            return structure

    def get_last_event(self, event_type: EventType, data_source_type: DataSourceType):
        with self.instance.lock.reader():
            event_count = len(self.instance.table_events)

            global last_event
            while True:
                last_event_raw = self.instance.table_events.get(doc_id=event_count)
                last_event = converter.structure(last_event_raw, Event)
                event_count -= 1
                if (last_event.event_type == event_type and last_event.data_source_type == data_source_type) or \
                    event_count < 1:
                    break

            return last_event


db = Database()
