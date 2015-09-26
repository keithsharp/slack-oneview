# Copyright 2015, Keith Sharp <keith.sharp@gmail.com>
#
# This file is part of Slack OneView.
#
# Slack OneView is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Slack OneView is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Slack OneView.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from setuptools import setup, find_packages
import codecs
import os
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

long_description = read('README.md')

setup(
    name='Slack OneView',
    version='0.1',
    description='An application to listen to the HP OneView SCMB and publish messages to Slack',
    long_description = long_description,
    author='Keith Sharp',
    author_email='keith.sharp@gmail.com',
    url='https://githup.com/keithsharp/slack-oneview',
    packages=['slack_oneview'],
    license='GPLv3',
    entry_points = {
        'console_scripts' : [
            'slack-oneview = slack_oneview.server:main',
            'ov-mq-keys' = 'slack_oneview.keys:main',
        ],
    },
    install_requires = [
        'amqp' >= 1.4.6,
        'hpOneView >= '0.1'
    ],
)
