#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/yes.py]

Defines the "yes" command.
"""

verbs = {}

def yes(env, args, kwargs):
    """[INT=1,...]@Returns a 'y' INT times."""
    try:
        return ["y"] * int(args[0])
    except IndexError:
        return ["y"]

verbs["yes"] = yes
