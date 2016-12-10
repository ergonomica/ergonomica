#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

verbs = {}

def _set(env, args, kwargs):
    """{KEY:VALUE,...}@Set the value of a variable."""
    for key in kwargs:
        env.namespace[key] = kwargs[key]
    return

verbs["set"] = _set
verbs["def"] = _set
verbs["var"] = _set
verbs["let"] = _set
