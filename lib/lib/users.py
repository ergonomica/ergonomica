#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/users.py]

Defines the "users" command.
"""

import subprocess

verbs = {}

def users(env, args, kwargs):
    """@Returns a list of currently logged in users."""
    try:
        return subprocess.check_output("w")
    except:
        print("'users' does not work on Windows computers.")
    
verbs["users"] = users
verbs["who"] = users
verbs["w"] = users
