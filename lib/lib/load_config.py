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
[lib/lib/load_config.py]

Defines the "load_config" command.
"""

from __future__ import print_function

import os
import sys
from lib.load.load_config import load_config

verbs = {}

def _load_config(env, args, kwargs):
    """@Load .ergo_profile."""
    try:
        LINES = open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile"), 'r').read().split("\n")
        LINES = [x for x in LINES if (x != "") and (x[0] != "#")] # filter out comments
        load_config(env, LINES)
    except IOError:
        _, error, _ = sys.exc_info()
        print("[ergo: ConfigError]: No such file ~/.ergo_profile. Please run ergo_setup." + str(error), file=sys.stderr)

verbs["load_config"] = _load_config
verbs["reload_config"] = _load_config
verbs["config_load"] = _load_config
verbs["config_reload"] = _load_config
