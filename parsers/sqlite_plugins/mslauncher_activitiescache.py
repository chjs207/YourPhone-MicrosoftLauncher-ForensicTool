# -*- coding: utf-8 -*-
"""This file contains a parser for the MSLauncher Notes.
"""

from __future__ import unicode_literals

from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class MSLauncherActivitiesCacheEventData(events.EventData):
    """MSLauncher Activities Cache Event data.
    """
    DATA_TYPE = 'mslauncher:event:activitiescache'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherActivitiesCacheEventData, self).__init__(data_type=self.DATA_TYPE)
        self.app_id = None
        self.app_activity_id = None
        self.last_modified_time = None
        self.expiration_time = None
        self.created_in_cloud = None
        self.start_time = None
        self.end_time = None
        self.last_modified_on_time_client = None
        self.local_expiration_time = None


class MSLauncherActivitiesCachePlugin(interface.SQLitePlugin):
    """Parse MSLauncher Activities Cache"""
    NAME = 'mslauncher_activitiescache'
    DESCRIPTION = 'Parser for MSLauncher activitiescache SQLite database files.'

    # Define the needed queris.
    QUERIES = [
        ('SELECT AppId, AppActivityId, LastModifiedTime, ExpirationTime, CreatedInCloud, '
         'StartTime, EndTime, LastModifiedOnClient, LocalExpirationTime '
         ' FROM Activity', 'ParseActivitiesCacheRow')]

    REQUIRED_TABLES = frozenset(['Activity'])

    def ParseActivitiesCacheRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Activities Cache record row."""

        query_hash = hash(query)

        event_data = MSLauncherActivitiesCacheEventData()
        event_data.app_id = self._GetRowValue(query_hash, row, 'AppId')
        event_data.app_activity_id = self._GetRowValue(query_hash, row, 'AppActivityId')
        LastModifiedTime = self._GetRowValue(query_hash, row, 'LastModifiedTime')
        conv_LastModifiedTime = dfdatetime_posix_time.PosixTime(LastModifiedTime)
        event_data.last_modified_time = conv_LastModifiedTime.CopyToDateTimeString()
        CreatedInCloud = self._GetRowValue(query_hash, row, 'CreatedInCloud')
        conv_CreatedInCloud = dfdatetime_posix_time.PosixTime(CreatedInCloud)
        event_data.created_in_cloud = conv_CreatedInCloud.CopyToDateTimeString()
        StartTime = self._GetRowValue(query_hash, row, 'StartTime')
        conv_StartTime = dfdatetime_posix_time.PosixTime(StartTime)
        event_data.start_time = conv_StartTime.CopyToDateTimeString()
        EndTime = self._GetRowValue(query_hash, row, 'EndTime')
        conv_EndTime = dfdatetime_posix_time.PosixTime(EndTime)
        event_data.end_time = conv_EndTime.CopyToDateTimeString()

        event = time_events.DateTimeValuesEvent(conv_StartTime, definitions.TIME_DESCRIPTION_CREATION)
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(MSLauncherActivitiesCachePlugin)
