#!/usr/bin/env python
# Copyright 2017, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Helper to upload Jenkins test results to BQ"""

from __future__ import print_function

import sys
import json
import csv
import os

columns = [
  ('jenkins_build', 'integer'),
  ('jenkins_suite', 'string'),
  ('test_name', 'string'),
  ('date', 'timestamp'),
  ('language', 'string'),
  ('platform', 'string'),
  ('config', 'string'),
  ('result', 'string'),
  ('test_duration', 'float'),
  ('cpu_estimated', 'float'),
  ('cpu_measured', 'float'),
]


def _populate_metadata_inplace(scenario_result):
  """Populates metadata based on environment variables set by Jenkins."""
  build_number = os.getenv('BUILD_NUMBER')
  build_url = os.getenv('BUILD_URL')
  job_name = os.getenv('JOB_NAME')
  git_commit = os.getenv('GIT_COMMIT')
  # Actual commit is the actual head of PR that is getting tested
  git_actual_commit = os.getenv('ghprbActualCommit')

  utc_timestamp = str(calendar.timegm(time.gmtime()))
  metadata = {'created': utc_timestamp}

  if build_number:
    metadata['buildNumber'] = build_number
  if build_url:
    metadata['buildUrl'] = build_url
  if job_name:
    metadata['jobName'] = job_name
  if git_commit:
    metadata['gitCommit'] = git_commit
  if git_actual_commit:
    metadata['gitActualCommit'] = git_actual_commit

  scenario_result['metadata'] = metadata
