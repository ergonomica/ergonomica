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

verbs = {}

def list_modules(env, args, kwargs):
    """@List all installed modules.."""
    files = os.listdir(os.path.join(os.path.join(os.path.expanduser("~") , ".ergo"), "packages"))
    return [f.replace(".py", "") for f in files if not f.endswith(".pyc")]
    
verbs["list_modules"] = list_modules
