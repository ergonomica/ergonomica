#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/nequal.py]

Defines the "nequal" command.
"""

verbs = {}

def nequal(env, args, kwargs):
    """[STRING,...]@Prints its input."""
    return args[0] != args[1]

verbs["nequal"] = nequal
