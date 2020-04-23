# -*- coding: utf-8 -*-
"""This file contains a parser for the YourPhone Settings.db.
"""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class YourPhoneSettingsEventData(events.EventData):
    """YourPhone Contacts Event data.

    """
    DATA_TYPE = 'yourphone:event:settingsdb'

    def __init__(self):
        """Initializes event data."""
        super(YourPhoneSettingsEventData, self).__init__(data_type=self.DATA_TYPE)
        self.app_name = None
        self.package_name = None
        self.version = None

class YourPhoneSettingsPlugin(interface.SQLitePlugin):
    """Parse YourPhone Settings.db"""
    NAME = 'yourphone_settingsdb'
    DESCRIPTION = 'Parser for YourPhone settings SQLite database files.'

    REQUIRED_TABLES = frozenset(['phone_apps'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT app_name, package_name, version FROM phone_apps', 'ParseSettingsRow')]

    def ParseSettingsRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Settings db record row."""

        query_hash = hash(query)

        event_data = YourPhoneSettingsEventData()
        event_data.app_name = self._GetRowValue(query_hash, row, 'app_name')
        event_data.package_name = self._GetRowValue(query_hash, row, 'package_name')
        event_data.version = self._GetRowValue(query_hash, row, 'version')

        date_time = dfdatetime_filetime.Filetime(timestamp=0)
        event = time_events.DateTimeValuesEvent(date_time, definitions.TIME_DESCRIPTION_UNKNOWN)
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(YourPhoneSettingsPlugin)