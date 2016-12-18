#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/export.py]

Defines the "export" command.
"""

import os
from lib.lang.error import ErgonomicaError

verbs = {}

def export(env, args, kwargs):
    """EXP,..@Append a line to .ergo_profile."""
    try:
        open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile"), 'w').write(" ".join(args) + "\n")
    except IOError:
        raise ErgonomicaError("[ergo: ConfigError]: .ergo_profile could not be found. Please run ergo_setup.")
    
verbs["export"] = export
