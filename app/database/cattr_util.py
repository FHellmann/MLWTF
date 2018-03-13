#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from datetime import datetime
from cattr import Converter


def _to_timestamp(dtime : datetime):
    return dtime.timestamp()

def _from_timestamp(timestamp : float, cls):
    return datetime.fromtimestamp(timestamp)


converter = Converter()
converter.register_structure_hook(datetime, _from_timestamp)
converter.register_unstructure_hook(datetime, _to_timestamp)
