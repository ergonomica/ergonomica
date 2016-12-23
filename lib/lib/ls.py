#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# imported from different file
# pylint: disable=import-error

"""
[lib/lib/ls.py]

Defines the "ls" command.
"""

import os
import re
import sys
import datetime
from lib.lang.stat import creation_date
from lib.lang.error import ErgonomicaError

verbs = {}

def ls(env, args, kwargs):
    """[DIR,...]@List files in a directory."""
    _long = False
    try:
        if kwargs["long"] in ["true", "t"]:
            _long = True
    except KeyError:
        pass

    # date processing from numerical time
    d = lambda t: str(datetime.datetime.fromtimestamp(creation_date(t))) + " " if _long else ""

    if len(args) > 1:
        return [d(item) + item for sublist in [ls(env, [x], kwargs) for x in args] for item in sublist]

    try:
        if len(args) == 0:
            return [env.theme["files"] + d(x) + x for x in os.listdir(env.directory)]
        return [args[0] + ":\n"] + [env.theme["files"] + d(x) + x for x in os.listdir(args[0])] + [""]
    except OSError:
        _, error, _ = sys.exc_info()
        raise ErgonomicaError("[ergo: NoSuchDirectoryError] No such directory '%s'." % (re.findall(r"'(.*?)'", str(error))[0]))

verbs["ls"] = ls
verbs["list"] = ls
