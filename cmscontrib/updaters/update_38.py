#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2018 Luca Wehrstedt <luca.wehrstedt@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A class to update a dump created by CMS.

Used by DumpImporter and DumpUpdater.

Add default values to the task type parameters of Communication for the
newly-introduced fields 'compilation' and 'user_io'.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins.disabled import *  # noqa
from future.builtins import *  # noqa
from six import iteritems

import json


class Updater(object):

    def __init__(self, data):
        assert data["_version"] == 37
        self.objs = data

    def run(self):
        for k, v in iteritems(self.objs):
            if k.startswith("_"):
                continue
            if v["_class"] == "Dataset" and v["task_type"] == "Communication":
                try:
                    params = json.loads(v["task_type_parameters"])
                except json.JSONDecodeError:
                    pass
                else:
                    if len(params) == 1:
                        params.extend(["stub", "fifo_io"])
                    v["task_type_parameters"] = json.dumps(params)

        return self.objs
