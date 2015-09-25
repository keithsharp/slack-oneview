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

import os
import sys
import time
import argparse

import hpOneView as hpov

def generate_certificates(con):
    print('Generating certificates .', end="")
    act = hpov.activity(con)
    request = {'type' : 'RabbitMqClientCertV2', 'commonName' : 'default'}
    (task, _) = con.post(hpov.common.uri['rabbitmq'], request)
    count = 0
    while act.is_task_running(task):
        print('.', end="")
        time.sleep(1)
        count += 1
        if count > 60:
            print(' timed out generating certificates.')
            sys.exit(1)

    task = con.get(task['uri'])
    if task['taskState'] in TaskErrorStates and task['taskState'] != 'Warning':
        message = task['taskErrors'][0]['message']
        print(' failed', end="")
        if message is not None:
            print(': ' + message)
        else:
            print('.')
        sys.exit(1)
    print(' done.')

def get_root_ca_bundle(con, dir):
    sec = hpov.security(con)
    cert = sec.get_cert_ca()
    ca = open(os.path.join(dir, 'caroot.pem'), 'w+')
    ca.write(cert)
    ca.close()

def get_certificate_pair(con, dir):
    sec = hpov.security(con)
    cert = sec.get_rabbitmq_kp()
    ca = open(os.path.join(dir, 'cert.pem'), 'w+')
    ca.write(cert['base64SSLCertData'])
    ca.close()
    ca = open(os.path.join(dir, 'key.pem'), 'w+')
    ca.write(cert['base64SSLKeyData'])
    ca.close()

def main():
    parser = argparse.ArgumentParser(description='Generate and download AMQP keys from HP OneView')
    parser.add_argument('-s', '--server', required=True, help='OneView server name or IP address')
    parser.add_argument('-u', '--username', required=True, help='OneView admin username')
    parser.add_argument('-p', '--password', required=True, help='Oneview admin password')
    parser.add_argument('-d', '--directory', default='.', help='Directory in which to create key files')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate the keypair before download')
    args = parser.parse_args()

    con = hpov.connection(args.server)

    try:
        con.login({'userName' : args.username, 'password' : args.password})
    except:
        print('Login failed, please check server name, username, and password.')
        sys.exit(1)

    if args.generate:
        generate_certificates(con)

    get_root_ca_bundle(con, args.directory)
    get_certificate_pair(con, args.directory)

    sys.exit(0)

if __name__ == '__main__':
    main()
