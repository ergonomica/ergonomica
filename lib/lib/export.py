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
[lib/lib/export.py]

Defines the "export" command.
"""

import os
from lib.lang.error import ErgonomicaError

verbs = {}

def export(env, args, kwargs):
    """[EXP,..]@Append a line to .ergo_profile."""
    try:
        open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile"), 'a').write(" ".join(args) + "\n")
    except IOError:
        raise ErgonomicaError("[ergo: ConfigError]: .ergo_profile could not be found. Please run ergo_setup.")
    
verbs["export"] = export
