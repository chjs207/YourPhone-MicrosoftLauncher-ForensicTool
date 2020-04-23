# -*- coding: utf-8 -*-
"""This file contains a parser for the YourPhone Call History.
"""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface

class YourPhoneCallEventData(events.EventData):
    """YourPhone Call Event data.

    """
    DATA_TYPE = 'yourphone:event:call'

    def __init__(self):
        """Initializes event data."""
        super(YourPhoneCallEventData, self).__init__(data_type=self.DATA_TYPE)
        self.phone_number = None
        self.duration = None
        self.call_type = None
        self.start_time = None
        self.last_updated_time = None

class YourPhoneCallPlugin(interface.SQLitePlugin):
    """Parse YourPhone """
    NAME = 'yourphone_calls'
    DESCRIPTION = 'Parser for YourPhone calls SQLite database files.'

    REQUIRED_TABLES = frozenset(['call_history'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT phone_number, duration, call_type, start_time, last_updated_time '
         'FROM call_history', 'ParseCallsRow')]

    CALL_TYPE = {
        1: 'INCOMING',
        2: 'OUTGOING',
        3: 'MISSED',
        5: 'DENY'
    }

    def ParseCallsRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Call record row."""

        query_hash = hash(query)

        event_data = YourPhoneCallEventData()
        call_type = self._GetRowValue(query_hash, row, 'call_type')
        event_data.call_type = self.CALL_TYPE.get(call_type, 'UNKNOWN')
        event_data.phone_number = self._GetRowValue(query_hash, row, 'phone_number')
        event_data.duration = self._GetRowValue(query_hash, row, 'duration')
        start_time = self._GetRowValue(query_hash, row, 'start_time')
        conv_start_time = dfdatetime_filetime.Filetime(timestamp=start_time)
        last_updated_time = self._GetRowValue(query_hash, row, 'last_updated_time')
        conv_last_updated_time = dfdatetime_filetime.Filetime(timestamp=last_updated_time)
        event_data.start_time = conv_start_time.CopyToDateTimeString()
        event_data.last_updated_time = conv_last_updated_time.CopyToDateTimeString()

        event = time_events.DateTimeValuesEvent(conv_start_time, 'Call Started')
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(YourPhoneCallPlugin)
