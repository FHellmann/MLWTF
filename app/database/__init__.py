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

_LOGGER = logging.getLogger(__name__)


class Database(object):
    def __init__(self):
        # Default: use in-memory database
        self.db = TinyDB(storage=MemoryStorage)
        self.table_events = None
        self.table_users = None
        self.table_devices = None
        self.setup(None)

    def __del__(self):
        self.db.close()

    def setup(self, path):
        if not (path is None):
            self.db = TinyDB(path)

        self.table_events = self.db.table('events')
        self.table_users = self.db.table('users')
        self.table_devices = self.db.table('devices')

    def add_event(self, data, event_type: EventType, data_source_type: DataSourceType):
        event = Event(event_type=event_type, data_source_type=data_source_type, data=data)
        unstructure = converter.unstructure(event)
        self.table_events.insert(unstructure)
        return event

    def get_event(self, event_id: int):
        event = self.table_events.get(doc_id=event_id)
        return event

    def get_events_by(self, event_type: EventType, data_source_type: DataSourceType,
                      since: datetime = datetime.utcnow()):
        search = self.table_events.search(
            (Query().event_type == event_type.value) &
            (Query().data_source_type == data_source_type.value) &
            (Query().timestamp >= since.timestamp())
        )
        structure = converter.structure(search, List[Event])
        return structure


db = Database()
