# -*- coding: utf-8 -*-
"""The YourPhone Photos formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class YourPhonePhotosEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a YourPhone Photos table record."""

  DATA_TYPE = 'yourphone:event:photos'

  FORMAT_STRING_PIECES = [
      'Name: {name}',
      'Last Updated Time: {last_updated_time}',
      'Taken Time: {taken_time}',
      'Size: {size}',
      'URI: {uri}',
      'Thumbnail: {thumbnail}',
      'Media: {media}']

  FORMAT_STRING_SHORT_PIECES = [
      'Name: {name}']

  SOURCE_LONG = 'YourPhonePhotos'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(YourPhonePhotosEventFormatter)
