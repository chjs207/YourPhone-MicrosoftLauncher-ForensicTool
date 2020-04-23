# -*- coding: utf-8 -*-
"""The MSLauncher ActivitiesCache event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MSLauncherActivitiesCacheEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a MSLauncher ActivitiesCache table record."""

  DATA_TYPE = 'mslauncher:event:activitiescache'

  FORMAT_STRING_PIECES = [
      'AppId: {app_id}',
      'AppActivityId: {app_activity_id}',
      'LastModifiedTime: {last_modified_time}',
      'ExpirationTime: {expiration_time}',
      'CreatedInCloud: {created_in_cloud}',
      'StartTime: {start_time}', 'EndTime: {end_time}',
      'LastModifiedOnTimeClient: {last_modified_on_time_client}',
      'LocalExpirationTime: {local_expiration_time}']

  FORMAT_STRING_SHORT_PIECES = [
      'AppId: {app_id}']

  SOURCE_LONG = 'MSLauncherActivitiesCache'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(MSLauncherActivitiesCacheEventFormatter)
