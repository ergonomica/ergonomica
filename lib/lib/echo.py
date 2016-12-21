#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

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
