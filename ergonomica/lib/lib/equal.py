#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/equal.py]

Defines the "equal" command.
"""

verbs = {}

def equal(env, args):
    """STRING1 STRING2@Returns STRING1 == STRING2."""
    return args[0] == args[1]

verbs["equal"] = equal
