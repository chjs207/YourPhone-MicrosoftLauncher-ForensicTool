# -*- coding: utf-8 -*-
"""The YourPhone Settings formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class YourPhoneSettingsDatabaseEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a YourPhone Settings Database table record."""

  DATA_TYPE = 'yourphone:event:settingsdb'

  FORMAT_STRING_PIECES = [
      'App name: {app_name}',
      'Package name: {package_name}',
      'App version: {version}']

  FORMAT_STRING_SHORT_PIECES = [
      'App name: {app_name}']

  SOURCE_LONG = 'YourPhoneSettingsDatabase'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(YourPhoneSettingsDatabaseEventFormatter)
