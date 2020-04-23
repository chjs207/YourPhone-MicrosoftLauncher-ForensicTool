# -*- coding: utf-8 -*-
"""YourPhone Call event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class YourPhoneCallEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a YourPhone Call table record."""

  DATA_TYPE = 'yourphone:event:call'

  FORMAT_STRING_PIECES = [
      'Phone number: {phone_number}',
      'Duration: {duration}',
      'Call type: {call_type}',
      'Start time: {start_time}',
      'Last Updated time: {last_updated_time}']

  FORMAT_STRING_SHORT_PIECES = [
      'Phone number: {phone_number}']

  SOURCE_LONG = 'YourPhoneCall'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(YourPhoneCallEventFormatter)
