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

import ssl
import amqp

class OneViewServer(object):

    def __init__(self, server, username, password):
        self._server = server
        self._username = username
        self._password = password

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def connect_to_scmb(self):
        ssl_options = {'ca_certs' : self._caroots,
                       'certfile' : self._certfile,
                       'keyfile' : self._keyfile,
                       'cert_reqs' : ssl.CERT_REQUIRED,
                       'ssl_version' : ssl.PROTOCOL_TLSv1_1,
                       'server_side' : FALSE}

        con = amqp.Connection(self._server + ':5671', login_method='EXTERNAL',
                              ssl=ssl_options)
        ch = conn.channel()
        qname, _, _ = ch.queue_declare()
        ch.queue_bind(qname, 'scmb', route)
        ch.basic_consume(qname, callback=partial(callback, ch))

        while ch.callbacks:
            ch.wait

        ch.close()
        con.close()
