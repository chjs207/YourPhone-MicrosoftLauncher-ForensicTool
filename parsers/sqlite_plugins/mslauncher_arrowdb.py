# -*- coding: utf-8 -*-
"""This file contains a parser for the MSLauncher arrow.
"""

from __future__ import unicode_literals

from dfdatetime import posix_time as dfdatetime_posix

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface

class MSLauncherArrowFrequencyEventData(events.EventData):
    """MSLauncher Arrow Frequency Event data.
    """
    DATA_TYPE = 'mslauncher:event:arrow_frequency'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherArrowFrequencyEventData, self).__init__(data_type=self.DATA_TYPE)
        self.package_name = None
        self.class_name = None
        self.frequency = None

class MSLauncherArrowFrequencyPlugin(interface.SQLitePlugin):
    """Parse MSLauncher Arrow Frequency"""
    NAME = 'mslauncher_arrowfrequency'
    DESCRIPTION = 'Parser for MSLauncher arrow frequency SQLite database files.'

    REQUIRED_TABLES = frozenset(['Frequency'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT packageName, className, frequency FROM Frequency', 'ParseArrowFrequencyRow')]

    def ParseArrowFrequencyRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Arrow Frequency record row."""

        query_hash = hash(query)

        event_data = MSLauncherArrowFrequencyEventData()
        event_data.package_name = self._GetRowValue(query_hash, row, 'packageName')
        event_data.class_name = self._GetRowValue(query_hash, row, 'className')
        event_data.frequency = self._GetRowValue(query_hash, row, 'frequency')
        datetime = dfdatetime_posix.PosixTime(timestamp=0)
        event = time_events.DateTimeValuesEvent(datetime, definitions.TIME_DESCRIPTION_UNKNOWN)
        parser_mediator.ProduceEventWithEventData(event, event_data)

class MSLauncherArrowReminderFoldersEventData():
    """MSLauncher Arrow Reminders Event data.
    """
    DATA_TYPE = 'mslauncher:event:arrow_reminderfolders'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherArrowReminderFoldersEventData, self).__init__(data_type=self.DATA_TYPE)
        self.name = None
        self.create_time = None

class MSLauncherArrowReminderFoldersPlugin(interface.SQLitePlugin):
    """Parse MSLauncher Arrow Reminder Folders"""
    NAME = 'mslauncher_arrowreminderfolders'
    DESCRIPTION = 'Parser for MSLauncher arrow reminderfolders SQLite database files.'

    REQUIRED_TABLES = frozenset(['ReminderFolders'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT name, createTime FROM ReminderFolders', 'ParseArrowReminderFoldersRow')]

    def ParseArrowReminderFoldersRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Arrow ReminderFolders record row."""

        query_hash = hash(query)

        event_data = MSLauncherArrowReminderFoldersEventData()
        event_data.name = self._GetRowValue(query_hash, row, 'name')
        event_data.create_time = self._GetRowValue(query_hash, row, 'createTime')
        datetime = dfdatetime_posix.PosixTime(timestamp=0)
        event = time_events.DateTimeValuesEvent(datetime, definitions.TIME_DESCRIPTION_UNKNOWN)
        parser_mediator.ProduceEventWithEventData(event, event_data)

class MSLauncherArrowRemindersEventData():
    """MSLauncher Arrow Reminders Event data.
    """
    DATA_TYPE = 'mslauncher:event:arrow_reminders'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherArrowRemindersEventData, self).__init__(data_type=self.DATA_TYPE)
        self.title = None
        self.create_time = None
        self.uuid = None
        self.folder = None

class MSLauncherArrowRemindersPlugin(interface.SQLitePlugin):
    """Parse MSLauncher Arrow Reminders"""
    NAME = 'mslauncher_arrowreminders'
    DESCRIPTION = 'Parser for MSLauncher arrow reminders SQLite database files.'

    REQUIRED_TABLES = frozenset(['Reminders'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT rm.title, rm.createTime, rm.uuid, rf.name as folder '
         'FROM Reminders rm INNER JOIN ReminderFolders rf '
         'ON rm.folderId == rf.id', 'ParseArrowRemindersRow')]

    def ParseArrowRemindersRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Arrow Reminders record row."""

        query_hash = hash(query)

        event_data = MSLauncherArrowRemindersEventData()
        event_data.title = self._GetRowValue(query_hash, row, 'title')
        event_data.create_time = self._GetRowValue(query_hash, row, 'createTime')
        event_data.uuid = self._GetRowValue(query_hash, row, 'uuid')
        event_data.folder = self._GetRowValue(query_hash, row, 'folder')
        datetime = dfdatetime_posix.PosixTime(timestamp=0)
        event = time_events.DateTimeValuesEvent(datetime, definitions.TIME_DESCRIPTION_UNKNOWN)
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugins\
    ([MSLauncherArrowFrequencyPlugin,
      MSLauncherArrowReminderFoldersPlugin,
      MSLauncherArrowRemindersPlugin])
