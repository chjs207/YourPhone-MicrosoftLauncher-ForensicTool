# -*- coding: utf-8 -*-
"""The YourPhone Contacts formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class YourPhoneContactEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a YourPhone Contacts table record."""

  DATA_TYPE = 'yourphone:event:contacts'

  FORMAT_STRING_PIECES = [
      'Display Name: {display_name}',
      'Nickname: {nickname}',
      'Last Updated time: {last_updated_time}',
      'Company: {company}',
      'Job: {job_title}', 'Notes: {notes}',
      'Name Prefix: {name_prefix}',
      'Name Suffix: {name_suffix}',
      'Given Name: {given_name}',
      'Middle Name: {middle_name}',
      'Family Name: {family_name}',
      'Phone number: {phone_number}',
      'Display Number: {display_number}',
      'Phone Number Type: {phone_number_type}']

  FORMAT_STRING_SHORT_PIECES = [
      'Display Name: {display_name}']

  SOURCE_LONG = 'YourPhoneContacts'
  SOURCE_SHORT = 'DATABASE'

manager.FormattersManager.RegisterFormatter(YourPhoneContactEventFormatter)
