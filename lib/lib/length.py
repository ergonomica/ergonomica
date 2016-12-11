#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/length.py]

Defines the "length" command.
"""

verbs = {}

def length(env, args, kwargs):
    """[STRING,...] {name:PATTERN=*}@Returns the length of its input."""
    return len(args)

verbs["length"] = length
verbs["len"] = length
