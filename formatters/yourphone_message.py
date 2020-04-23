# -*- coding: utf-8 -*-
"""The YourPhone Message formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class YourPhoneMessageEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a YourPhone Message table record."""

  DATA_TYPE = 'yourphone:event:message'

  FORMAT_STRING_PIECES = [
      'Message type: {message_type}',
      'Phone number: {from_address}',
      'Message: {body}',
      'Timestamp: {timestamp}']

  FORMAT_STRING_SHORT_PIECES = [
      'Message: {body}']

  SOURCE_LONG = 'YourPhoneMessage'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(YourPhoneMessageEventFormatter)
