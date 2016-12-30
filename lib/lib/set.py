#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/set.py]

Defines the "set" command.
"""

verbs = {}

def _set(env, args, kwargs):
    """{KEY:VALUE,...}@Set the value of each KEY to its corresponding VALUE."""
    for key in kwargs:
        env.namespace[key] = kwargs[key]
    return

verbs["set"] = _set
verbs["def"] = _set
verbs["var"] = _set
verbs["let"] = _set
