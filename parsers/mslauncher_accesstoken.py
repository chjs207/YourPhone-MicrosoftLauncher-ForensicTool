# -*- coding: utf-8 -*-
"""Parser for the MSLauncher AccessToken.xml files."""

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

class MSLauncherAccessTokenEventData(events.EventData):
    """MSLauncher AccessToken event data.

    Attributes:
        accessToken (str)
        accountId (str)
        displayName (str)
        expireOn (str)
        firstName (str)
        lastName (str)
        refreshToken (str)
        userName (str)
    """

    DATA_TYPE = 'mslauncher:event:accesstoken'

    def __init__(self):
        """Initializes event data."""
        super(MSLauncherAccessTokenEventData, self).__init__(data_type=self.DATA_TYPE)
        self.appname = ''
        self.access_token = ''
        self.account_id = ''
        self.display_name = ''
        self.expire_one = ''
        self.first_name = ''
        self.last_name = ''
        self.refresh_token = ''
        self.user_name = ''

class MSLauncherAccessTokenParser(interface.FileObjectParser):
    """Parses MSLauncher AccessToken.xml file-like object"""

    NAME = 'mslauncher_accesstoken'
    DESCRIPTION = 'Parser for MSLauncher AccessToken xml files.'

    _HEADER_READ_SIZE = 128

    def ParseFileObject(self, parser_mediator, file_object):
        """Parses MS Launcher AccessToken file-like object.

        Args:
            parser_mediator (ParserMediator): mediates interactions between parsers
                and other components, such as storage and dfvfs.
            file_object (dfvfs.FileIO): file-like object.

        Raises:
            unableToParseFile: when the file cannot be parsed.
        """
        data = file_object.read(self._HEADER_READ_SIZE)
        if not data.startswith(b'<?xml'):
            raise errors.UnableToParseFile(
                'Not a MSLauncher AccessToken.xml file [not XML]')

        _, _, data = data.partition(b'\n')
        if not data.startswith(b'<map>'):
            raise errors.UnableToParseFile(
                'Not a MSLauncher AccessToken.xml file [wrong XML tag]')

        _, _, data = data.partition(b'\n')
        if not data.startswith(b'    <string'):
            raise errors.UnableToParseFile(
                'Not a MSLauncher AccessToken.xml file [wrong XML tag]')

        # the current offset of the file-like object needs to point at
        # the start of the file for ElementTree to parse the XML data correctly.
        file_object.seek(0, os.SEEK_SET)

        xml = ElementTree.parse(file_object)
        root_node = xml.getroot()
        event_data = MSLauncherAccessTokenEventData()

        for sub_node in root_node:
            str_name = str(sub_node.get('name'))
            if not 'AccessToken' in str_name:
                return
            event_data.appname = str_name
            split_text = str(sub_node.text).split(',')
            for text in split_text:
                if 'accessToken' in text:
                    text = text.replace("&quot;", '')
                    text = text.split(':')
                    event_data.access_token = text[1]
                    continue
                elif 'accountId' in text:
                    text = text.replace("&quot;", '')
                    text = text.split(':')
                    event_data.account_id = text[1]
                    continue
                elif 'displayName' in text:
                    text = text.replace("&quot;", '')
                    text = text.split(':')
                    event_data.display_name = text[1]
                    continue
                elif 'expireOne' in text:
                    text = text.replace("&quot;", '')
                    text = text.split(':')
                    event_data.expire_one = text[1]
                    continue
                elif 'firstName' in text:
                    text = text.replace("&quot;", '')
                    text = text.split(':')
                    event_data.first_name = text[1]
                    continue
                elif 'lastName' in text:
                    text = text.replace("&quot;", '')
                    text = text.split(':')
                    event_data.last_name = text[1]
                    continue
                elif 'refreshToken' in text:
                    text = text.replace("&quot;", '')
                    text = text.split(':')
                    event_data.refresh_token = text[1]
                    continue
                elif 'userName' in text:
                    text = text.replace("&quot;", '')
                    text = text.split(':')
                    event_data.user_name = text[1]
                    continue
                else:
                    continue
            date_time = dfdatetime_posix_time.PosixTime(timestamp=0)
            event = time_events.DateTimeValuesEvent(
                date_time, definitions.TIME_DESCRIPTION_UNKNOWN)
            parser_mediator.ProduceEventWithEventData(event, event_data)
            continue

manager.ParsersManager.RegisterParser(MSLauncherAccessTokenParser)