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
    """[DIR,...]List files in a directory."""

    _long = False
    if "-long" in args:
        _long = True
        
    # date processing from numerical time
    d = lambda t: str(datetime.datetime.fromtimestamp(creation_date(t))) + " " if _long else ""

    if len(args) > 1:
        out = [ls(env, [x]) for x in args]

        # flatten
        return [item for sublist in out for item in sublist]

    try:
        if len(args) == 0:
            return [env.theme["files"] + d(x) + x for x in os.listdir(env.directory)]

        dir = [args[0] + ":"]
        out = [env.theme["files"] + d(args[0] + "/" + x) + x for x in os.listdir(args[0])]
        return dir + out
    except OSError:
        _, error, _ = sys.exc_info()
        bad_dir = re.findall(r"'(.*?)'", str(error))[0]
        raise ErgonomicaError("[ergo: NoSuchDirectoryError] No such directory '%s'." % (bad_dir))

verbs["ls"] = ls
verbs["list"] = ls
