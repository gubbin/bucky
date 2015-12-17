# -*- coding: utf-8 -
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# Copyright 2011 Cloudant, Inc.

import six
import sys
import time
import socket
import struct
import logging
try:
    import cPickle as pickle
except ImportError:
    import pickle

import bucky.client as client
import bucky.names as names


if six.PY3:
    xrange = range


log = logging.getLogger(__name__)


class DebugSocket(object):
    def sendall(self, data):
        sys.stdout.write(data)


class CarbonClient(client.Client):
    def __init__(self, cfg, pipe):
        super(CarbonClient, self).__init__(pipe)
        self.debug = cfg.debug
        self.ip = cfg.graphite_ip
        self.port = cfg.graphite_port
        self.max_reconnects = cfg.graphite_max_reconnects
        self.reconnect_delay = cfg.graphite_reconnect_delay
        self.backoff_factor = cfg.graphite_backoff_factor
        self.backoff_max = cfg.graphite_backoff_max
        if self.max_reconnects <= 0:
            self.max_reconnects = sys.maxint
        self.connect()

    def connect(self):
        log.debug("Connected the debug socket.")
        self.sock = DebugSocket()
        return

    def reconnect(self):
        self.close()
        self.connect()

    def close(self):
        try:
            self.sock.close()
        except:
            pass


class PlaintextClient(CarbonClient):
    def send(self, host, name, value, mtime):
        stat = names.statname(host, name)
        mesg = "%s %s %s\n" % (stat, value, mtime)
        print "mesg:", mesg,

