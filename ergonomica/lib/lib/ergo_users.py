#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_users.py]

Defines the "users" command.
"""

import subprocess


def users(argc):
    """users: Returns a list of currently logged in users.

    Usage:
        users
    """

    try:
        return subprocess.check_output("w")
    except OSError:
        print("'users' does not work on Windows computers.")


exports = {'users': users}
