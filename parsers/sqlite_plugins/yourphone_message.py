# -*- coding: utf-8 -*-
"""This file contains a parser for the YourPhone Message.
"""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface

class YourPhoneMessageEventData(events.EventData):
    """YourPhone SMS Event data.

    """
    DATA_TYPE = 'yourphone:event:message'

    def __init__(self):
        """Initializes event data."""
        super(YourPhoneMessageEventData, self).__init__(data_type=self.DATA_TYPE)
        self.message_type = None
        self.from_address = None
        self.body = None
        self.timestamp = None

class YourPhoneMessagePlugin(interface.SQLitePlugin):
    """Parse YourPhone """
    NAME = 'yourphone_message'
    DESCRIPTION = 'Parser for YourPhone messages SQLite database files.'

    REQUIRED_TABLES = frozenset(['message', 'mms', 'mms_part', 'subscription'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT mms.from_address, mms.type, mms_part.text as body, mms.timestamp '
         'FROM mms INNER JOIN mms_part ON mms.message_id == mms_part.message_id', 'ParseMMStableRow'),
        ('SELECT from_address, type, body, timestamp FROM message', 'ParseMessagetableRow')]

    MESSAGE_TYPE = {
        1: 'INCOMING',
        2: 'OUTGOING'
    }

    def ParseMMStableRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a mms table record row."""

        query_hash = hash(query)

        event_data = YourPhoneMessageEventData()

        message_type = self._GetRowValue(query_hash, row, 'type')
        event_data.message_type = self.MESSAGE_TYPE.get(message_type, 'UNKNONW')
        event_data.body = self._GetRowValue(query_hash, row, 'body')
        timestamp = self._GetRowValue(query_hash, row, 'timestamp')
        conv_timestamp = dfdatetime_filetime.Filetime(timestamp=timestamp)
        event_data.timestamp = conv_timestamp.CopyToDateTimeString()

        if message_type == 1:
            event_data.from_address = self._GetRowValue(query_hash, row, 'from_address')
            event = time_events.DateTimeValuesEvent(conv_timestamp, 'Message Received')
            parser_mediator.ProduceEventWithEventData(event, event_data)
        else:
            event_data.from_address = 'User'
            event = time_events.DateTimeValuesEvent(conv_timestamp, 'Message Sent')
            parser_mediator.ProduceEventWithEventData(event, event_data)

    def ParseMessagetableRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a message table record row."""

        query_hash = hash(query)

        event_data = YourPhoneMessageEventData()

        message_type = self._GetRowValue(query_hash, row, 'type')
        event_data.message_type = self.MESSAGE_TYPE.get(message_type, 'UNKNOWN')
        event_data.body = self._GetRowValue(query_hash, row, 'body')
        timestamp = self._GetRowValue(query_hash, row, 'timestamp')
        conv_timestamp = dfdatetime_filetime.Filetime(timestamp=timestamp)
        event_data.timestamp = conv_timestamp.CopyToDateTimeString()
        if message_type == 1:
            event_data.from_address = self._GetRowValue(query_hash, row, 'from_address')
            event = time_events.DateTimeValuesEvent(conv_timestamp, 'Message Received')
            parser_mediator.ProduceEventWithEventData(event, event_data)
        else:
            event_data.from_address = 'User'
            event = time_events.DateTimeValuesEvent(conv_timestamp, 'Message Sent')
            parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(YourPhoneMessagePlugin)
