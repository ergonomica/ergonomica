#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/echo.py]

Defines the "echo"/"print" command.
"""

verbs = {}

def equal(env, args, kwargs):
    """[STRING,...]@Prints its input."""
    return args[0] == args[1]

verbs["equal"] = equal
