# -*- coding: utf-8 -*-
"""This file contains a parser for the MSLauncher Bingsearchhistory.
"""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface

class MSLauncherBingSearchHistoryEventData(events.EventData):
    """MSLauncher BingSearchHistory Event data.
    """
    DATA_TYPE = 'mslauncher:event:bingsearchhistory'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherBingSearchHistoryEventData, self).__init__(data_type=self.DATA_TYPE)
        self.query_string = None
        self.url = None
        self.last = None

class MSLauncherBingSearchHistoryPlugin(interface.SQLitePlugin):
    """Parse MSLauncher Arrow Frequency"""
    NAME = 'mslauncher_bingsearchhistory'
    DESCRIPTION = 'Parser for MSLauncher bing searchhistory SQLite database files.'

    REQUIRED_TABLES = frozenset(['BingSearchHistory'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT _QUERY_STRING, _URL, _LAST FROM BingSearchHistory', 'ParseBingSearchHistoryRow')]

    def ParseBingSearchHistoryRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a BingSearchHistory record row."""

        query_hash = hash(query)

        event_data = MSLauncherBingSearchHistoryEventData()
        event_data.query_string = self._GetRowValue(query_hash, row, '_QUERY_STRING')
        event_data.url = self._GetRowValue(query_hash, row, '_URL')
        event_data.last = self._GetRowValue(query_hash, row, '_LAST')
        date_time = dfdatetime_filetime.Filetime(timestamp=0)
        event = time_events.DateTimeValuesEvent(date_time, definitions.TIME_DESCRIPTION_UNKNOWN)
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(MSLauncherBingSearchHistoryPlugin)
