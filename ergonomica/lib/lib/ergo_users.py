#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/users.py]

Defines the "users" command.
"""

import subprocess


def ergo_users(argc):
    """users: Returns a list of currently logged in users.

    Usage:
        users
    """

    try:
        return subprocess.check_output("w")
    except:
        print("'users' does not work on Windows computers.")
