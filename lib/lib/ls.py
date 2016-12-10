#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/ls.py]

Defines the "ls" command.
"""

import os
import re
from lib.lang.error import ErgonomicaError

verbs = {}

def ls(env, args, kwargs):
    """[DIR,...]@List files in a directory."""
    if len(args) > 1:
        return [item for sublist in [ls(env, [x], kwargs) for x in args] for item in sublist]
    try:
        if len(args) == 0:
            return os.listdir(env.directory)
        return [args[0] + ":\n"] + os.listdir(args[0]) + [""]
    except OSError, error:
        raise ErgonomicaError("[ergo: NoSuchDirectoryError] No such directory '%s'." % (re.findall(r"'(.*?)'", str(error))[0]))

verbs["ls"] = ls
verbs["list"] = ls
