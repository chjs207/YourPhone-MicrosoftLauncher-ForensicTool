# -*- coding: utf-8 -*-
"""The YourPhone DeviceData formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class YourPhoneDeviceDataEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a YourPhone DeviceData table record."""

  DATA_TYPE = 'yourphone:event:devicedata'

  FORMAT_STRING_PIECES = [
      'WallPaper: {blob}']

  FORMAT_STRING_SHORT_PIECES = [
      'WallPaper: {blob}']

  SOURCE_LONG = 'YourPhoneDeviceData'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(YourPhoneDeviceDataEventFormatter)
