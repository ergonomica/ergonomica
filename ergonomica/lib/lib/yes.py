#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/yes.py]

Defines the "yes" command.
"""

verbs = {}

def yes(env, args, kwargs):
    """[INT=1] {string:y\\n}@Returns a 'y' INT times."""
    try:
        s = kwargs["string"]
    except KeyError:
        s = "y\n"
    try:
        return s * int(args[0])
    except IndexError:
        return s

verbs["yes"] = yes
