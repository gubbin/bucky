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

import sys
import time
import logging

import bucky.client as client
import bucky.names as names


log = logging.getLogger(__name__)


class CarbonClient(client.Client):
    def __init__(self, cfg, pipe):
        super(CarbonClient, self).__init__(pipe)
        self.debug = cfg.debug

    def close(self):
        pass


class PlaintextClient(CarbonClient):
    def send(self, host, name, value, mtime):
        stat = names.statname(host, name)
        mesg = "%s %s %s" % (stat, mtime, value)
        print mesg

