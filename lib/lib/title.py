#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/title.py]

Defines the "title" command.
"""

import sys
from lib.lang.error import ErgonomicaError

verbs = {}

def title(env, args, kwargs):
    """TITLE@Set the title of the current terminal window."""
    if len(args) != 1:
        raise ErgonomicaError("[ergo: ArgumentError]: Incorrect number of arguments passed to 'title'.")
    sys.stdout.write("\x1b]2;%s\x07" % (args[0]))
    return
        
verbs["title"] = title
