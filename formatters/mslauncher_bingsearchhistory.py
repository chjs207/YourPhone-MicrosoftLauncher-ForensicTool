# -*- coding: utf-8 -*-
"""The MSLauncher BingSearchHistory event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MSLauncherBingSearchHistoryEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a MSLauncher BingSearchHistory table record."""

  DATA_TYPE = 'mslauncher:event:bingsearchhistory'

  FORMAT_STRING_PIECES = [
      'keyword: {query_string}',
      'url: {url}',
      'search date: {last}']

  FORMAT_STRING_SHORT_PIECES = [
      'keyword: {query_string}']

  SOURCE_LONG = 'MSLauncherBingSearchHistory'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(MSLauncherBingSearchHistoryEventFormatter)
