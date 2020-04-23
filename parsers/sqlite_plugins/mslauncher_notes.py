# -*- coding: utf-8 -*-
"""This file contains a parser for the MSLauncher Notes.
"""

from __future__ import unicode_literals

from dfdatetime import java_time as dfdatetime_java

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class MSLauncherNotesEventData(events.EventData):
    """MSLauncher Arrow Frequency Event data.
    """
    DATA_TYPE = 'mslauncher:event:notes'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherNotesEventData, self).__init__(data_type=self.DATA_TYPE)
        self.local_created_at = None
        self.document_modified_at = None
        self.remote_data = None
        self.document = None
        self.created_by_app = None

class MSLauncherNotesPlugin(interface.SQLitePlugin):
    """Parse MSLauncher Notes"""
    NAME = 'mslauncher_notes'
    DESCRIPTION = 'Parser for MSLauncher notes SQLite database files.'

    REQUIRED_TABLES = frozenset(['Note'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT localCreatedAt, documentModifiedAt, remoteData, document, createdByApp'
         ' FROM Note', 'ParseNotesRow')]

    def ParseNotesRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Notes record row."""

        query_hash = hash(query)

        event_data = MSLauncherNotesEventData()
        localCreatedAt = self._GetRowValue(query_hash, row, 'localCreatedAt')
        conv_localCreatedAt = dfdatetime_java.JavaTime(timestamp=localCreatedAt)
        event_data.local_created_at = conv_localCreatedAt.CopyToDateTimeString()
        documentModifiedAt = self._GetRowValue(query_hash, row, 'documentModifiedAt')
        conv_documentModifiedAt = dfdatetime_java.JavaTime(timestamp=documentModifiedAt)
        event_data.document_modified_at = conv_documentModifiedAt.CopyToDateTimeString()
        event_data.remoteData = self._GetRowValue(query_hash, row, 'remoteData')
        event_data.document = self._GetRowValue(query_hash, row, 'document')
        event_data.created_by_app = self._GetRowValue(query_hash, row, 'createdByApp')

        event = time_events.DateTimeValuesEvent(conv_localCreatedAt, definitions.TIME_DESCRIPTION_CREATION)
        parser_mediator.ProduceEventWithEventData(event, event_data)
        event = time_events.DateTimeValuesEvent(conv_documentModifiedAt, definitions.TIME_DESCRIPTION_MODIFICATION)
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(MSLauncherNotesPlugin)
