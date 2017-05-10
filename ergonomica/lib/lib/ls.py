#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ls.py]

Defines the "ls" command.
"""

import os
import re
import sys
import datetime
from ergonomica.lib.lang.stat import creation_date
from ergonomica.lib.lang.error import ErgonomicaError

verbs = {}

def ls(env, args):
    """[DIR=.] [--date]@List all files in DIR. If -d specified, shows file creation dates."""

    # date processing from numerical time
    d = lambda t: str(datetime.datetime.fromtimestamp(creation_date(t))) + " " if args['--date'] else ""

    return [env.theme["files"] + d(x) + x for x in os.listdir(env.directory)]


verbs["ls"] = ls
verbs["list"] = ls
