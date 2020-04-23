# -*- coding: utf-8 -*-
"""The MSLauncher Cookies event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MSLauncherFamilyMembersCacheKeyEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a MSLauncher Family_Members_Cache_Key file."""

  DATA_TYPE = 'mslauncher:event:familymemberscachekey'

  FORMAT_STRING_PIECES = [
      'Account Primary Alias: {account_primary_alias}',
      'Who: {owner}']

  FORMAT_STRING_SHORT_PIECES = [
      'Account Primary Alias: {account_primary_alias}']

  SOURCE_LONG = 'MSLauncherFamilyMembersCacheKey'
  SOURCE_SHORT = 'LOG'

manager.FormattersManager.RegisterFormatter(MSLauncherFamilyMembersCacheKeyEventFormatter)
