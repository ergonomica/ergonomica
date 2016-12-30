#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/nequal.py]

Defines the "nequal" command.
"""

verbs = {}

def nequal(env, args, kwargs):
    """STR1 STR2@Returns STR1 != STR2."""
    return args[0] != args[1]

verbs["nequal"] = nequal
