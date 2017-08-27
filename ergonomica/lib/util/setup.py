#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/util/setup.py]

The Ergonomica setup script.
"""

import os
import requests
import sqlite3

# this is used for py2-3 cross-compatibility
# pylint: disable=redefined-builtin, invalid-name
try:
    input = raw_input
except NameError:
    pass

def setup():
    """
    Set up the users computer for Ergonomica. Note that this is only
    called when it is known that their computer does not have this structure
    is installed.
    """

    user_dir = os.path.expanduser("~")

    os.mkdir(os.path.join(user_dir, ".ergo"))
    os.mkdir(os.path.join(user_dir, ".ergo", "packages"))
    open(os.path.join(user_dir, ".ergo", ".ergo_profile"), "w")
    open(os.path.join(user_dir, ".ergo", ".ergo_history"), "w")
    open(os.path.join(user_dir, ".ergo", "packages", "__init__.py"), "w")