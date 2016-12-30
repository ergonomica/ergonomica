#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/macro.py]

Defines the "macro" command.
"""

verbs = {}

def macro(env, args, kwargs):
    """STRING REPLACEMENT_STRING@Defines a text macro."""
    env.macros[args[0]] = args[1]

verbs["macro"] = macro
