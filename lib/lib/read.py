#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/read.py]

Defines the "read" command.
"""

verbs = {}

def read(env, args, kwargs):
    """[FILE,...]@Read a file."""
    return [item for sublist in [open(x, "r").read().split("\n") for x in args] for item in sublist]

verbs["read"] = read
verbs["cat"] = read
