# -*- coding: utf-8 -*-
"""This file contains a parser for the YourPhone Smartphone Wallpaper.
"""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface
import binascii

class YourPhoneDeviceDataEventData(events.EventData):
    """YourPhone DeviceData Event data.

    """
    DATA_TYPE = 'yourphone:event:devicedata'

    def __init__(self):
        """Initializes event data."""
        super(YourPhoneDeviceDataEventData, self).__init__(data_type=self.DATA_TYPE)
        self.blob = None

class YourPhoneDeviceDataPlugin(interface.SQLitePlugin):
    """Parse YourPhone DeviceData"""
    NAME = 'yourphone_devicedata'
    DESCRIPTION = 'Parser for YourPhone devicedata SQLite database files.'

    REQUIRED_TABLES = frozenset(['wallpaper'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT wallpaper_id, blob FROM wallpaper', 'ParseDeviceDataRow')]

    def ParseDeviceDataRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Contact record row."""

        query_hash = hash(query)

        event_data = YourPhoneDeviceDataEventData()
        blob = self._GetRowValue(query_hash, row, 'blob')
        event_data.blob = binascii.b2a_hex(blob)

        event_data.blob = self._GetRowValue(query_hash, row, 'blob')
        date_time = dfdatetime_filetime.Filetime(timestamp=0)
        event = time_events.DateTimeValuesEvent(date_time, definitions.TIME_DESCRIPTION_UNKNOWN)
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(YourPhoneDeviceDataPlugin)