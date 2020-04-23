# -*- coding: utf-8 -*-
"""This file contains a parser for the YourPhone Notifications.
"""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class YourPhoneNotificationEventData(events.EventData):
    """YourPhone Notifications Event data.

    """
    DATA_TYPE = 'yourphone:event:notifications'

    def __init__(self):
        """Initializes event data."""
        super(YourPhoneNotificationEventData, self).__init__(data_type=self.DATA_TYPE)
        self.notification_id = None
        self.json = None
        self.post_time = None


class YourPhoneNotificationPlugin(interface.SQLitePlugin):
    """Parse YourPhone Notification"""
    NAME = 'yourphone_notifications'
    DESCRIPTION = 'Parser for YourPhone notifications SQLite database files.'

    REQUIRED_TABLES = frozenset(['notifications'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT notification_id, json, post_time FROM notifications', 'ParseNotificationsRow')]

    def ParseNotificationsRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Notification record row."""

        query_hash = hash(query)

        event_data = YourPhoneNotificationEventData()
        event_data.notification_id = self._GetRowValue(query_hash, row, 'notification_id')
        event_data.json = self._GetRowValue(query_hash, row, 'json')
        post_time = self._GetRowValue(query_hash, row, 'post_time')
        conv_post_time = dfdatetime_filetime.Filetime(timestamp=post_time)
        event_data.post_time = conv_post_time.CopyToDateTimeString()

        event = time_events.DateTimeValuesEvent(conv_post_time, 'POST_TIME')
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(YourPhoneNotificationPlugin)
