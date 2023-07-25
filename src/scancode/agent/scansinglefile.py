#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2023  Sushant Kumar (sushsnatmishra02102002@gmail.com)

SPDX-License-Identifier: LGPL-2.1

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

import json
import argparse

def update_license(licenses):
  """
  Extracts relevant information from the 'licenses' data.
  Parameters:
    licenses (dict): A dictionary containing license information.
  Returns:
    list: A list of dictionaries containing relevant license information.
  """
  updated_licenses = []
  keys_to_extract_from_licenses = ['key', 'score', 'name', 'text_url', 'start_line', 'matched_text']

  for key, value in licenses.items():
    if key == 'licenses':
      for license in value:
        updated_licenses.append({key: license[key] for key in keys_to_extract_from_licenses if key in license})

  return updated_licenses

def update_copyright(copyrights):
  """
  Extracts relevant information from the 'copyrights' data.
  Parameters:
    copyrights (dict): A dictionary containing copyright information.
  Returns:
    tuple: A tuple of two lists. The first list contains updated copyright information,
    and the second list contains updated holder information.
  """
  updated_copyrights = []
  updated_holders = []
  keys_to_extract_from_copyrights = ['copyright', 'start_line']
  keys_to_extract_from_holders = ['holder', 'start_line']
  key_mapping = {
    'start_line': 'start',
    'copyright': 'value',
    'holder': 'value'
  }

  for key, value in copyrights.items():
    if key == 'copyrights':
      for copyright in value:
        updated_copyrights.append({key_mapping.get(key, key): copyright[key] for key in keys_to_extract_from_copyrights if key in copyright})
    if key == 'holders':
      for holder in value:
        updated_holders.append({key_mapping.get(key, key): holder[key] for key in keys_to_extract_from_holders if key in holder})
  return updated_copyrights, updated_holders

def update_emails(emails):
  """
  Extracts relevant information from the 'emails' data.
  Parameters:
    emails (dict): A dictionary containing email information.
  Returns:
    list: A list of dictionaries containing relevant email information.
  """
  updated_emails = []
  keys_to_extract_from_emails = ['email', 'start_line']
  key_mapping = {
    'start_line': 'start',
    'email': 'value'
  }

  for key, value in emails.items():
    if key == 'emails':
      for email in value:
        updated_emails.append({key_mapping.get(key, key): email[key] for key in keys_to_extract_from_emails if key in email})

  return updated_emails

def update_urls(urls):
  """
  Extracts relevant information from the 'urls' data.
  Parameters:
    urls (dict): A dictionary containing url information.
  Returns:
    list: A list of dictionaries containing relevant url information.
  """
  updated_urls = []
  keys_to_extract_from_urls = ['url', 'start_line']
  key_mapping = {
    'start_line': 'start',
    'url': 'value'
  }

  for key, value in urls.items():
    if key == 'urls':
      for url in value:
        updated_urls.append({key_mapping.get(key, key): url[key] for key in keys_to_extract_from_urls if key in url})

  return updated_urls

def process_file(file_location, scan_copyrights, scan_licenses, scan_emails, scan_urls):
  """
  Process a file and extract copyright and/or license information.
  Parameters:
    file_location (str): The location of the file to be processed.
    scan_copyrights (bool): If True, scan for copyright information.
    scan_licenses (bool): If True, scan for license information.
  Outputs:
    Prints the extracted copyright and/or license information in JSON format.
  """
  from scancode import api

  result = {}
  result['licenses'] = []
  result['copyrights'] = []
  result['holders'] = []
  result['emails'] = []
  result['urls'] = []

  if scan_copyrights:
    copyrights = api.get_copyrights(file_location)
    updated_copyrights, updated_holders = update_copyright(copyrights)
    result['copyrights'] = updated_copyrights
    result['holders'] = updated_holders

  if scan_licenses:
    licenses = api.get_licenses(file_location, include_text=True)
    updated_licenses = update_license(licenses)
    result['licenses'] = updated_licenses

  if scan_emails:
    emails = api.get_emails(file_location)
    updated_emails = update_emails(emails)
    result['emails'] = updated_emails

  if scan_urls:
    urls = api.get_urls(file_location)
    updated_urls = update_urls(urls)
    result['urls'] = updated_urls

  print(json.dumps(result))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Process a file specified by its location.")
  parser.add_argument("file_location", help="Location of the file to be processed")
  parser.add_argument("-c", "--scan-copyrights", action="store_true", help="Scan for copyrights")
  parser.add_argument("-l", "--scan-licenses", action="store_true", help="Scan for licenses")
  parser.add_argument("-e", "--scan-emails", action="store_true", help="Scan for emails")
  parser.add_argument("-u", "--scan-urls", action="store_true", help="Scan for urls")

  args = parser.parse_args()
  file_location = args.file_location
  scan_copyrights = args.scan_copyrights
  scan_licenses = args.scan_licenses
  scan_emails = args.scan_emails
  scan_urls = args.scan_urls

  process_file(file_location, scan_copyrights, scan_licenses, scan_emails, scan_urls)
