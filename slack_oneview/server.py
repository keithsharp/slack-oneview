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
import amqp
import ssl

from oneview import OneViewServer
from slack import SlackServer

def parse_config_file(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)

    ov = OneViewServer(config['oneview']['server'],
                       config['oneview']['username'],
                       config['oneview']['password'],
                       config['oneview']['certfile'],
                       config['oneview']['keyfile'],
                       config['oneview']['caroot'],)

    ss = SlackServer(config['slack']['webhook'],
                     config['slack']['botname'],
                     config['slack']['channel'])

    return (ov, ss)

def on_message(channel, method_frame, header_frame, body):
    print('Got a message!')
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def main():
    parser = argparse.ArgumentParser(description='Listen on the HP OneView SCMB and publish messages to Slack.')
    parser.add_argument('-f', '--file', required=True, help='Path to the config file')
    args = parser.parse_args()
    (ov, ss) = parse_config_file(args.file)

    ssl_options = {'ca_certs' : ov.caroot,
                   'certfile' : ov.certfile,
                   'keyfile' : ov.keyfile,
                   'cert_reqs' : ssl.CERT_REQUIRED,
                   'ssl_version' : ssl.PROTOCOL_TLSv1_1,
                   'server_side' : False}

    con = amqp.Connection(ov.server + ':5671', login_method='EXTERNAL', ssl=ssl_options)

    con.close()

if __name__ == '__main__':
    main()

    https://github.com/HewlettPackard/python-hpOneView.git
