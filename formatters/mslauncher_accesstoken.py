# -*- coding: utf-8 -*-
"""The MSLauncher Cookies event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class MSLauncherAccessTokenEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a MSLauncher AccessToken XML."""

  DATA_TYPE = 'mslauncher:event:accesstoken'

  FORMAT_STRING_PIECES = [
      'Application: {appname}',
      'AccessToken: {access_token}',
      'Account: {account_id}',
      'Display Name: {display_name}',
      'Expire: {expire_one}',
      'First Name: {first_name}',
      'Last Name: {last_name}',
      'RefreshToken: {refresh_token}',
      'User Name: {user_name}']

  FORMAT_STRING_SHORT_PIECES = [
      'Application: {appname}']

  SOURCE_LONG = 'MSLauncherAccessToken'
  SOURCE_SHORT = 'XML'

manager.FormattersManager.RegisterFormatter(MSLauncherAccessTokenEventFormatter)
