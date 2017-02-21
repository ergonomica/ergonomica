#!/usr/bin/python
# -*- coding: utf-8 -*-

# no other way to do it
# pylint: disable=line-too-long

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/title.py]

Defines the "title" command.
"""

import sys
from lib.lang.error import ErgonomicaError

verbs = {}

def title(env, args, kwargs):
    """TITLE@Set the title of the current terminal window to TITLE."""
    if len(args) != 1:
        raise ErgonomicaError("[ergo: ArgumentError]: Incorrect number of arguments passed to 'title'.")
    sys.stdout.write("\x1b]2;%s\x07" % (args[0]))
    return

verbs["title"] = title
