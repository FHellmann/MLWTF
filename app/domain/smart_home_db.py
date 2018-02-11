#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from tinydb import TinyDB, Query


class SmartHomeDb:
    def __init__(self):
        self.db = TinyDB('smart_home_db.json')

    def insert(self, json):
        self.db.insert(json)
