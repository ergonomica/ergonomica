#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/macro.py]

Defines the "macro" command.
"""

verbs = {}

def macro(env, args):
    """STRING REPLACEMENT_STRING@Defines a text macro mapping STRING to REPLACEMENT_STRING."""
    env.macros[args[0]] = args[1]

verbs["macro"] = macro
