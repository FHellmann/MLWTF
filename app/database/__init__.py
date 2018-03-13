#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

_LOGGER = logging.getLogger(__name__)


class Database(object):
    def __init__(self):
        # Default: use in-memory database
        self.db = TinyDB(storage=MemoryStorage)

    def __del__(self):
        self.db.close()

    def setup(self, path):
        if not(path is None):
            self.db = TinyDB(path)

    def get(self):
        return self.db

db = Database()
