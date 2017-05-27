#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/length.py]

Defines the "length" command.
"""

verbs = {}

def length(env, args, kwargs):
    """[STRING,...]@Returns the number of arguments passed."""
    return len(args)

verbs["length"] = length
verbs["len"] = length
