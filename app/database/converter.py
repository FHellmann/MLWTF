#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from datetime import datetime
from cattr import Converter
from .models import DataSource, DataSourceType


converter = Converter()

converter.register_structure_hook(datetime, lambda timestamp, cls: datetime.fromtimestamp(timestamp))
converter.register_unstructure_hook(datetime, lambda dtime: dtime.timestamp())

converter.register_structure_hook(DataSource, lambda event_type_name, cls: DataSource(event_type_name))

converter.register_structure_hook(DataSourceType, lambda ds_type_name, cls: DataSourceType(ds_type_name))
