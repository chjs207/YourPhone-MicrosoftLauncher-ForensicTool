# -*- coding: utf-8 -*-
"""The MSLauncher Arrow Frequency event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MSLauncherArrowFrequencyEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a MSLauncher ArrowFrequency table record."""

  DATA_TYPE = 'mslauncher:event:arrow_frequency'

  FORMAT_STRING_PIECES = [
      'packageName: {package_name}',
      'className: {class_name}',
      'frequency: {frequency}']

  FORMAT_STRING_SHORT_PIECES = [
      'AppId: {app_id}']

  SOURCE_LONG = 'MSLauncherArrowFrequency'
  SOURCE_SHORT = 'DATABASE'

class MSLauncherArrowReminderFoldersEventFormatter(interface.ConditionalEventFormatter):
    """Formatter for a MSLauncher ArrowReminderFolders table record."""
    DATA_TYPE = 'mslauncher:event:arrow_reminderfolders'

    FORMAT_STRING_PIECES = [
        'name: {name}',
        'create time: {create_time}']

    FORMAT_STRING_SHORT_PIECES = [
        'name: {name}']

    SOURCE_LONG = 'MSLauncherArrowReminderFolders'
    SOURCE_SHORT = 'DATABASE'

class MSLauncherArrowRemindersEventFormatter(interface.ConditionalEventFormatter):
    """Formatter for a MSLauncher ArrowReminders table record."""
    DATA_TYPE = 'mslauncher:event:arrow_reminders'

    FORMAT_STRING_PIECES = [
        'title: {title}',
        'create time: {create_time}',
        'uuid: {uuid}',
        'folder: {folder}']

    FORMAT_STRING_SHORT_PIECES = [
        'title: {title}']

    SOURCE_LONG = 'MSLauncherArrowReminders'
    SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatters([
    MSLauncherArrowFrequencyEventFormatter,
    MSLauncherArrowReminderFoldersEventFormatter,
    MSLauncherArrowRemindersEventFormatter])