# -*- coding: utf-8 -*-
"""This file contains a parser for the MSLauncher cookies.
"""

from __future__ import unicode_literals

from dfdatetime import webkit_time as dfdatetime_webkit_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface

class MSLauncherCookiesEventData(events.EventData):
    """MSLauncher Cookies Event data.

    Attributes:
        creation_utc (str)
        host_key (str)
        value (str)
        last_access_utc (str)
    """
    DATA_TYPE = 'mslauncher:event:cookies'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherCookiesEventData, self).__init__(data_type=self.DATA_TYPE)
        self.creation_utc = None
        self.host_key = None
        self.value = None
        self.last_access_utc = None

class MSLauncherCookiesPlugin(interface.SQLitePlugin):
    """Parse MSLauncher Cookies"""
    NAME = 'mslauncher_cookies'
    DESCRIPTION = 'Parser for MSLauncher cookies SQLite database files.'

    # Define the needed queris.
    QUERIES = [
        ('SELECT creation_utc, host_key, value, last_access_utc FROM cookies', 'ParseCookiesRow')]

    REQUIRED_TABLES = frozenset(['cookies'])

    SCHEMAS = [{
        'cookies': (
        'CREATE TABLE cookies(creation_utc INTEGER NOT NULL,'
        'host_key TEXT NOT NULL,name TEXT NOT NULL,value TEXT NOT NULL,'
        'path TEXT NOT NULL,expires_utc INTEGER NOT NULL,is_secure INTEGER NOT NULL,'
        'is_httponly INTEGER NOT NULL,last_access_utc INTEGER NOT NULL,'
        'has_expires INTEGER NOT NULL DEFAULT 1,is_persistent INTEGER NOT NULL DEFAULT 1,'
        'priority INTEGER NOT NULL DEFAULT 1,encrypted_value BLOB DEFAULT '','
        'samesite INTEGER NOT NULL DEFAULT -1,source_scheme INTEGER NOT NULL DEFAULT 0,'
        'UNIQUE (host_key, name, path))'),
        'meta': (
        'CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR)')}]

    def ParseCookiesRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Cookies record row."""

        query_hash = hash(query)
        event_data = MSLauncherCookiesEventData()

        creation_utc = self._GetRowValue(query_hash, row, 'creation_utc')
        conv_creation_utc = dfdatetime_webkit_time.WebKitTime(creation_utc)
        event_data.creation_utc \
            = dfdatetime_webkit_time.WebKitTime(creation_utc).CopyToDateTimeString()
        event_data.host_key = self._GetRowValue(query_hash, row, 'host_key')
        event_data.value = self._GetRowValue(query_hash, row, 'value')
        last_access_utc = self._GetRowValue(query_hash, row, 'last_access_utc')
        conv_last_access_utc = dfdatetime_webkit_time.WebKitTime(last_access_utc)
        event_data.last_access_utc \
            = dfdatetime_webkit_time.WebKitTime(last_access_utc).CopyToDateTimeString()

        event = time_events.DateTimeValuesEvent(conv_creation_utc, definitions.TIME_DESCRIPTION_CREATION)
        parser_mediator.ProduceEventWithEventData(event, event_data)
        event = time_events.DateTimeValuesEvent(conv_last_access_utc, definitions.TIME_DESCRIPTION_LAST_ACCESS)
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(MSLauncherCookiesPlugin)
