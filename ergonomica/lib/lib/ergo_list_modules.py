#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/load_config.py]

Defines the "load_config" command.
"""

from __future__ import print_function
import os


def ergo_list_modules(env, args):
    """list_modules: List all installed modules.

    Usage:
        list_modules
    """
    
    files = os.listdir(os.path.join(os.path.join(os.path.expanduser("~") , ".ergo"), "packages"))
    return [f.replace(".py", "") for f in files if not f.endswith(".pyc")]
