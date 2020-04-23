# -*- coding: utf-8 -*-
"""File containing a Windows Registry plugin to parse the YourPhone settings.dat."""

from __future__ import unicode_literals

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import definitions
from plaso.lib import errors
from plaso.parsers import winreg
from plaso.parsers.winreg_plugins import interface


class YourPhoneSettingsDataEventData(events.EventData):
    """Windows Registry of YourPhone Settings.dat event data attribute container.
    """

    DATA_TYPE = 'yourphone:event:settingsdat'

    def __init__(self):
        """Initialize event data."""
        super(YourPhoneSettingsDataEventData, self).__init__(data_type=self.DATA_TYPE)
        self.key_path = None
        self.manufacturer = None
        self.model = None
        self.osversion = None
        self.contactslastupdatedtime = None
        self.messagelastupdatedtime = None
        self.callsdevicebluetoothaddress = None
        self.calllogslastupdatedtime = None
        self.phoneappslastupdatedtime = None
        self.mediainfolastupdatedtime = None

class YourPhoneSettingsDataPlugin(interface.WindowsRegistryPlugin):
    """Windows registry plugin for YourPhone settings.dat
    """
    NAME = 'windows_yourphone_settingsdat'
    DESCRIPTION = 'Parser for YourPhone settings.dat'

    FILTERS = frozenset([interface.WindowsRegistryKeyPathFilter(
        '\\LocalState\\Devices')])

    def ExtractEvents(self, parser_mediator, registry_key, **kwargs):
        """Extracts events from a Windows Registry key.
        """
        event_data = YourPhoneSettingsDataEventData()
        DeviceIDkey = None

        for subkey in registry_key.GetSubkeys():
            split_subkey_name = subkey.name.split('-')
            if len(split_subkey_name) == 5:
                try:
                    DeviceIDkey = subkey
                    for values in subkey.GetValues():
                        test = values.name
                        if 'Manufacturer' == values.name:
                            manufacturer = bytes(values.GetDataAsObject())[:-10]
                            event_data.manufacturer = manufacturer.decode('utf-16')
                            continue
                        elif 'Model' == values.name:
                            model = bytes(values.GetDataAsObject())[:-10]
                            event_data.model = model.decode('utf-16')
                            continue
                        elif 'OsVersion' == values.name:
                            osversion = bytes(values.GetDataAsObject())
                            event_data.osversion = int(osversion[0])
                            continue
                        elif 'ContactsLastUpdatedTime' == values.name:
                            contactslastupdatedtime = bytes(values.GetDataAsObject())[:8]
                            contactslastupdatedtime = int.from_bytes(contactslastupdatedtime, byteorder='little')
                            event_data.contactslastupdatedtime = dfdatetime_filetime.Filetime(contactslastupdatedtime).CopyToDateTimeString()
                            continue
                        elif 'MessagesLastUpdatedTime' == values.name:
                            messageslastupdatedtime = bytes(values.GetDataAsObject())[:8]
                            messageslastupdatedtime = int.from_bytes(messageslastupdatedtime, byteorder='little')
                            event_data.messagelastupdatedtime = dfdatetime_filetime.Filetime(messageslastupdatedtime).CopyToDateTimeString()
                            continue
                        elif 'CallsDeviceBluetoothAddress' == values.name:
                            callsdevicebluetoothaddress = bytes(values.GetDataAsObject())[:-10]
                            event_data.callsdevicebluetoothaddress = str(callsdevicebluetoothaddress)
                            continue
                        elif 'CallLogsLastUpdatedTime' == values.name:
                            calllogslastupdatedtime = bytes(values.GetDataAsObject())[:8]
                            calllogslastupdatedtime = int.from_bytes(calllogslastupdatedtime, byteorder='little')
                            event_data.calllogslastupdatedtime = dfdatetime_filetime.Filetime(calllogslastupdatedtime).CopyToDateTimeString()
                            continue
                        elif 'PhoneAppsLastUpdatedTime' == values.name:
                            phoneappslastupdatedtime = bytes(values.GetDataAsObject())[:8]
                            phoneappslastupdatedtime = int.from_bytes(phoneappslastupdatedtime, byteorder='little')
                            event_data.phoneappslastupdatedtime = dfdatetime_filetime.Filetime(phoneappslastupdatedtime).CopyToDateTimeString()
                            continue
                        elif 'MediaInfoLastUpdatedTime' == values.name:
                            mediainfolastupdatedtime = bytes(values.GetDataAsObject())[:8]
                            mediainfolastupdatedtime = int.from_bytes(mediainfolastupdatedtime, byteorder='little')
                            event_data.mediainfolastupdatedtime = dfdatetime_filetime.Filetime(mediainfolastupdatedtime).CopyToDateTimeString()
                            continue
                        else:
                            continue
                except:
                    errors.UnableToParseFile(
                        'Unable to parse Settings.dat of YourPhone')
                    return
        event = time_events.DateTimeValuesEvent(
            DeviceIDkey.last_written_time, definitions.TIME_DESCRIPTION_MODIFICATION)
        parser_mediator.ProduceEventWithEventData(event, event_data)

winreg.WinRegistryParser.RegisterPlugin(YourPhoneSettingsDataPlugin)