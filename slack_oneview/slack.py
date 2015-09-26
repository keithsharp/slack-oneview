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

import json
import urllib.parse
import urllib.request

class SlackServer(object):

    def __init__(self, webhook, botname, channel):
        self._webhook = webhook
        self._botname = botname
        self._channel = channel

    @property
    def webhook(self):
        return self._webhook

    @webhook.setter
    def webhook(self, value):
        self._webhook = value

    @property
    def botname(self):
        return self._botname

    @botname.setter
    def botname(self, value):
        self._botname = value

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    def post_message(self, message):
        payload = {"text" : message, "channel" : self.channel, "username" : self.botname}
        req = urllib.request.Request(self.webhook, data=json.dumps(payload).encode('utf-8'),
                                     headers={'content-type' : 'application/json'})
        response = urllib.request.urlopen(req)
