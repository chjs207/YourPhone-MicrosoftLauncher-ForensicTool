# -*- coding: utf-8 -*-
"""The MSLauncher Notes event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MSLauncherNotesEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a MSLauncher Notes table record."""

  DATA_TYPE = 'mslauncher:event:notes'

  FORMAT_STRING_PIECES = [
      'Local Created: {local_created_at}',
      'Modified: {document_modified_at}',
      'Remote Data: {remote_data}',
      'Document: {document}',
      'Created by App: {created_by_app}']

  FORMAT_STRING_SHORT_PIECES = [
      'Local Created: {local_created_at}']

  SOURCE_LONG = 'MSLauncherNotes'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(MSLauncherNotesEventFormatter)
