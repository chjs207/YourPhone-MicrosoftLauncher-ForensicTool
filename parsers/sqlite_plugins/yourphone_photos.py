# -*- coding: utf-8 -*-
"""This file contains a parser for the YourPhone Photos.
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


class YourPhonePhotosEventData(events.EventData):
    """YourPhone Photos Event data.

    """
    DATA_TYPE = 'yourphone:event:photos'

    def __init__(self):
        """Initializes event data."""
        super(YourPhonePhotosEventData, self).__init__(data_type=self.DATA_TYPE)
        self.name = None
        self.last_updated_time = None
        self.taken_time = None
        self.size = None
        self.uri = None
        self.thumbnail = None
        self.media = None


class YourPhonePhotosPlugin(interface.SQLitePlugin):
    """Parse YourPhone Photos"""
    NAME = 'yourphone_photos'
    DESCRIPTION = 'Parser for YourPhone photos SQLite database files.'

    REQUIRED_TABLES = frozenset(['media', 'photo'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT name, last_updated_time, taken_time, size, '
         'uri, thumbnail, media FROM media', 'ParseMediaRow'),
        ('SELECT name, last_updated_time, taken_time, size, '
         'uri, thumbnail, blob as media FROM photo', 'ParsePhotoRow')]


    def ParseMediaRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Media record row."""

        query_hash = hash(query)

        event_data = YourPhonePhotosEventData()
        event_data.name = self._GetRowValue(query_hash, row, 'name')
        event_data.size = self._GetRowValue(query_hash, row, 'size')
        event_data.uri = self._GetRowValue(query_hash, row, 'uri')
        thumbnail = self._GetRowValue(query_hash, row, 'thumbnail')
        event_data.thumbnail = binascii.b2a_hex(thumbnail)
        media = self._GetRowValue(query_hash, row, 'media')
        event_data.media = binascii.b2a_hex(media)

        last_updated_time = self._GetRowValue(query_hash, row, 'last_updated_time')
        conv_last_updated_time = dfdatetime_filetime.Filetime(timestamp=last_updated_time)

        taken_time = self._GetRowValue(query_hash, row, 'taken_time')
        conv_taken_time = dfdatetime_filetime.Filetime(timestamp=taken_time)

        event_data.last_updated_time = conv_last_updated_time.CopyToDateTimeString()
        event_data.taken_time = conv_taken_time.CopyToDateTimeString()

        event = time_events.DateTimeValuesEvent(conv_taken_time, 'Sync Time')
        parser_mediator.ProduceEventWithEventData(event, event_data)
        event = time_events.DataTimeValuesEvent(conv_last_updated_time, 'Last updated Time')
        parser_mediator.ProduceEventWithEventData(event, event_data)

    def ParsePhotoRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Photo record row"""

        query_hash = hash(query)

        event_data = YourPhonePhotosEventData()
        event_data.name = self._GetRowValue(query_hash, row, 'name')
        event_data.size = self._GetRowValue(query_hash, row, 'size')
        event_data.uri = self._GetRowValue(query_hash, row, 'uri')
        thumbnail = self._GetRowValue(query_hash, row, 'thumbnail')
        event_data.thumbnail = binascii.b2a_hex(thumbnail)
        media = self._GetRowValue(query_hash, row, 'media')
        event_data.media = binascii.b2a_hex(media)

        last_updated_time = self._GetRowValue(query_hash, row, 'last_updated_time')
        conv_last_updated_time = dfdatetime_filetime.Filetime(timestamp=last_updated_time)

        taken_time = self._GetRowValue(query_hash, row, 'taken_time')
        conv_taken_time = dfdatetime_filetime.Filetime(timestamp=taken_time)

        event_data.last_updated_time = conv_last_updated_time.CopyToDateTimeString()
        event_data.taken_time = conv_taken_time.CopyToDateTimeString()

        event = time_events.DateTimeValuesEvent(conv_last_updated_time, 'Last updated Time')
        parser_mediator.ProduceEventWithEventData(event, event_data)

        event = time_events.DateTimeValuesEvent(conv_taken_time, 'Sync Time')
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(YourPhonePhotosPlugin)
