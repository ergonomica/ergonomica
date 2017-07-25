#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/load_config.py]

Defines the "load_config" command.
"""

import os


def list_modules(argc):
    """list_modules: List all installed modules.

    Usage:
        list_modules
    """

    files = os.listdir(os.path.join(os.path.join(os.path.expanduser("~"), ".ergo"), "packages"))
    return [f.replace(".py", "") for f in files if not f.endswith(".pyc")]


exports = {'list_modules': list_modules}