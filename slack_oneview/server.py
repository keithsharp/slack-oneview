#!/usr/bin/env python3

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

import argparse
import configparser

from oneview import OneViewServer
from slack import SlackServer

def parse_config_file(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)

    ov = OneViewServer(config['oneview']['server'],
                       config['oneview']['username'],
                       config['oneview']['password'])

    ss = SlackServer(config['slack']['webhook'],
                     config['slack']['botname'],
                     config['slack']['channel'])

    return (ov, ss)

def main():
    parser = argparse.ArgumentParser(description='Listen on the HP OneView SCMB and publish messages to Slack.')
    parser.add_argument('-f', '--file', help='Path to the config file')
    args = parser.parse_args()
    (ov, ss) = parse_config_file(args.file)

    #print(ss.channel)
    ss.post_message("Hello, World!")

if __name__ == '__main__':
    main()
