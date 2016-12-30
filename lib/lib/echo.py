#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument


"""
[lib/lib/echo.py]

Defines the "echo"/"print" command.
"""

verbs = {}

def echo(env, args, kwargs):
    """[STRING,...]@Prints its input."""
    return args

verbs["echo"] = echo
verbs["print"] = echo
