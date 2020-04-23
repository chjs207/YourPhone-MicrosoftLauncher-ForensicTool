# -*- coding: utf-8 -*-
"""Parser for the MSLauncher Family_Members_Cache_Key files."""

from __future__ import unicode_literals

import os

from defusedxml import ElementTree
from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import errors
from plaso.lib import definitions
from plaso.parsers import interface
from plaso.parsers import manager

class MSLauncherFamilyMembersCacheKeyEventData(events.EventData):
    """Windows MSLauncher Family Members Cache Key event data.
    """

    DATA_TYPE = 'mslauncher:event:familymemberscachekey'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherFamilyMembersCacheKeyEventData, self).__init__(data_type=self.DATA_TYPE)
        self.account_primary_alias = ''
        self.is_caller = ''
        self.owner = ''

class MSLauncherFamilyMembersCacheKeyParser(interface.FileObjectParser):
    """Parses a MSLauncher FamilyMembersCacheKey file-like object"""

    NAME = 'mslauncher_familymemberscachekey'
    DESCRIPTION = 'Parser for Windows filehistory Config.xml files.'

    def ParseFileObject(self, parser_mediator, file_object):
        """Parses an Windows FileHistory Config file-like object.

        Args:
            parser_mediator (ParserMediator): mediates interactions between parsers
                and other components, such as storage and dfvfs.
            file_object (dfvfs.FileIO): file-like object.

        Raises:
            unableToParseFile: when the file cannot be parsed.
        """
        data = file_object.read(23)
        if not data.startswith(b'[{"accountPrimaryAlias"'):
            raise errors.UnableToParseFile(
                'Not MSLauncher FamilyMembersCacheKey file')

        event_data = MSLauncherFamilyMembersCacheKeyEventData()

        file_object.seek(0, os.SEEK_SET)

        data = file_object.read().decode('utf-8')[1:-1]
        split_data = data.split("}")
        for tmp1 in split_data:
            tmp1 = tmp1.replace("{", '')
            split_tmp1 = tmp1.split(',')
            for tmp2 in split_tmp1:
                if 'accountPrimaryAlias' in tmp2:
                    event_data.account_primary_alias = tmp2.replace('"accountPrimaryAlias":', '')
                    continue
                elif 'isCaller' in tmp2:
                    event_data.is_caller = tmp2.replace('"isCaller":', '')
                    if event_data.is_caller == 'false':
                        event_data.owner = 'Guest'
                        continue
                    else:
                        event_data.owner = 'Owner'
                        continue
                else:
                    continue
            event = time_events.DateTimeValuesEvent(
                None, definitions.TIME_DESCRIPTION_UNKNOWN)
            parser_mediator.ProduceEventWithEventData(event, event_data)

manager.ParsersManager.RegisterParser(MSLauncherFamilyMembersCacheKeyParser)