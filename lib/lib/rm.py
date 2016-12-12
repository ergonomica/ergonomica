#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/rm.py]

Defines the "rm" command.
"""

import os
from lib.lang.error import ErgonomicaError

verbs = {}

def rm(env, args, kwargs):
    """[PATH,...]@Remove files."""
    try:
        [os.remove(env.directory + "/" + x) for x in args]
    except OSError:
        raise ErgonomicaError("")
    return

verbs["rm"] = rm
verbs["remove"] = rm
