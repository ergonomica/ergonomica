#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/macro.py]

Defines the "macro" command.
"""


def ergo_macro(env, args):
    """ergo_macro: Defines a text macro mapping STRING to REPLACEMENT_STRING.

    Usage:
        ergo_macro STRING REPLACEMENT_STRING
    """
    
    env.macros[args[0]] = args[1]
