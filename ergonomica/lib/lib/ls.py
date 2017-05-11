#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ls.py]

Defines the "ls" command.
"""

import os
import datetime
from ergonomica.lib.lang.stat import creation_date

verbs = {}

def ls(args):
    """[DIR=.] [--date]@List all files in DIR. If --date specified, shows file creation dates."""

    # date processing from numerical time
    d = lambda t: str(datetime.datetime.fromtimestamp(creation_date(t))) + " " if args.args['--date'] else ""

    return [args.env.theme["files"] + d(x) + x for x in os.listdir(args.env.directory)]


verbs["ls"] = ls

