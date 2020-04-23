# -*- coding: utf-8 -*-
"""The YourPhone Settings Dat formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class YourPhoneSettingsDatEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a YourPhone Settings Registry record."""

  DATA_TYPE = 'yourphone:event:settingsdat'

  FORMAT_STRING_PIECES = [
      '[{key_path}]',
      'Manufacturer: {manufacturer}',
      'Model: {model}',
      'OS Version: {osversion}',
      'Contact Updated Time: {contactslastupdatedtime}',
      'Message Updated Time: {messagelastupdatedtime}',
      'Call Log Updated Time: {calllogslastupdatedtime}',
      'Phone Apps Updated Time: {phoneappslastupdatedtime}',
      'Media Updated Time: {mediainfolastupdatedtime}',
      'Call Bluetooth Address: {callsdevicebluetoothaddress}']

  FORMAT_STRING_SHORT_PIECES = [
      'Manufacturer: {manufacturer}']

  SOURCE_LONG = 'YourPhoneSettingsDat'
  SOURCE_SHORT = 'REG'

manager.FormattersManager.RegisterFormatter(YourPhoneSettingsDatEventFormatter)
