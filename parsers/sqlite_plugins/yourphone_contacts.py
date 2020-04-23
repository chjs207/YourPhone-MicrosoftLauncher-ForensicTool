# -*- coding: utf-8 -*-
"""This file contains a parser for the YourPhone Contacts.
"""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import py2to3
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class YourPhoneContactEventData(events.EventData):
    """YourPhone Contacts Event data.

    """
    DATA_TYPE = 'yourphone:event:contacts'

    def __init__(self):
        """Initializes event data."""
        super(YourPhoneContactEventData, self).__init__(data_type=self.DATA_TYPE)
        self.display_name = None
        self.nickname = None
        self.last_updated_time = None
        self.company = None
        self.job_title = None
        self.notes = None
        self.name_prefix = None
        self.name_suffix = None
        self.given_name = None
        self.middle_name = None
        self.family_name = None
        self.phone_number = None
        self.display_number = None
        self.phone_number_type = None

class YourPhoneContactPlugin(interface.SQLitePlugin):
    """Parse YourPhone Contact"""
    NAME = 'yourphone_contacts'
    DESCRIPTION = 'Parser for YourPhone contacts SQLite database files.'

    REQUIRED_TABLES = frozenset(['contact', 'phonenumber'])

    # Define the needed queris.
    QUERIES = [
        ('SELECT ct.display_name, ct.nickname, ct.last_updated_time, ct.company, '
         'ct.job_title, ct.notes, ct.name_prefix, ct.name_suffix, ct.given_name, '
         'ct.middle_name, ct.family_name, pn.phone_number, pn.display_phone_number, '
         'pn.phone_number_type FROM contact ct '
         'INNER JOIN phonenumber pn ON ct.contact_id == pn.contact_id', 'ParseContactsRow')]

    CONTACT_TYPE = {
        1: 'HOME',
        2: 'MOBILE',
        3: 'WORK',
        5: 'MAIN'
    }

    def ParseContactsRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses a Contact record row."""

        query_hash = hash(query)

        event_data = YourPhoneContactEventData()
        phone_number_type = self._GetRowValue(query_hash, row, 'phone_number_type')
        event_data.phone_number_type = self.CONTACT_TYPE.get(phone_number_type, 'UNKNOWN')
        event_data.display_name = self._GetRowValue(query_hash, row, 'display_name')
        event_data.nickname = self._GetRowValue(query_hash, row, 'nickname')
        event_data.company = self._GetRowValue(query_hash, row, 'company')
        event_data.job_title = self._GetRowValue(query_hash, row, 'job_title')
        event_data.notes = self._GetRowValue(query_hash, row, 'notes')
        event_data.name_prefix = self._GetRowValue(query_hash, row, 'name_prefix')
        event_data.name_suffix = self._GetRowValue(query_hash, row, 'name_suffix')
        event_data.given_name = self._GetRowValue(query_hash, row, 'given_name')
        event_data.middle_name = self._GetRowValue(query_hash, row, 'middle_name')
        event_data.family_name = self._GetRowValue(query_hash, row, 'family_name')
        event_data.phone_number = self._GetRowValue(query_hash, row, 'phone_number')

        last_updated_time = self._GetRowValue(query_hash, row, 'last_updated_time')
        conv_last_updated_time = dfdatetime_filetime.Filetime(timestamp=last_updated_time)
        event_data.last_updated_time = conv_last_updated_time.CopyToDateTimeString()

        event = time_events.DateTimeValuesEvent(conv_last_updated_time, definitions.TIME_DESCRIPTION_UNKNOWN)
        parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(YourPhoneContactPlugin)
