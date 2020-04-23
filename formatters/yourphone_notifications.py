# -*- coding: utf-8 -*-
"""The YourPhone Notifications formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class YourPhoneNotificationEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a YourPhone Notifications table record."""

  DATA_TYPE = 'yourphone:event:notifications'

  FORMAT_STRING_PIECES = [
      'Notification ID: {notification_id}',
      'Message: {json}',
      'Timestamp: {post_time}']

  FORMAT_STRING_SHORT_PIECES = [
      'Message: {json}']

  SOURCE_LONG = 'YourPhoneNotifications'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(YourPhoneNotificationEventFormatter)
