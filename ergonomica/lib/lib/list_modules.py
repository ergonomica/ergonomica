#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/load_config.py]

Defines the "load_config" command.
"""

from __future__ import print_function

import os

verbs = {}

def list_modules(env, args):
    """@List all installed modules.."""
    files = os.listdir(os.path.join(os.path.join(os.path.expanduser("~") , ".ergo"), "packages"))
    return [f.replace(".py", "") for f in files if not f.endswith(".pyc")]
    
verbs["list_modules"] = list_modules
