# -*- coding: utf-8 -*-
"""The MSLauncher Cookies event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MSLauncherCookiesEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a MSLauncher Cookies table record."""

  DATA_TYPE = 'mslauncher:event:cookies'

  FORMAT_STRING_PIECES = [
      'Created Time: {creation_utc}',
      'Host key: {host_key}',
      'Value: {value}',
      'Last Access Time: {last_access_utc}']

  FORMAT_STRING_SHORT_PIECES = [
      'Created Time: {creation_utc}']

  SOURCE_LONG = 'MSLauncherCookies'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(MSLauncherCookiesEventFormatter)
