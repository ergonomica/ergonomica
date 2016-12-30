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
[lib/lib/rm.py]

Defines the "rm" command.
"""

import os
from lib.lang.error import ErgonomicaError

verbs = {}

def rm(env, args, kwargs):
    """[FILE,...]@Remove FILEs (works for directories as well)."""
    try:
        [os.remove(env.directory + "/" + x) for x in args]
    except OSError:
        raise ErgonomicaError("")
    return

verbs["rm"] = rm
verbs["remove"] = rm
