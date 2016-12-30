#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/read.py]

Defines the "read" command.
"""

import re
from lib.lang.error import ErgonomicaError

verbs = {}

def read(env, args, kwargs):
    """[FILE,...]@Read all FILEs."""
    try:
        return [item for sublist in [open(x, "r").read().split("\n") for x in args] for item in sublist]
    except IOError as error:
        raise ErgonomicaError("[ergo: FileError]: No such readable file '%s'" % (re.findall(r"'(.*?)'", str(error))[0]))

verbs["read"] = read
verbs["cat"] = read
