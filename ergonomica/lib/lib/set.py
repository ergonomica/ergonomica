#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/set.py]

Defines the "set" command.
"""

verbs = {}

def _set(env, ns, args):
    """VAR VAL@Returns the number of arguments passed."""
    ns[args['VAR']] = args['VAL']
    return

verbs["set"] = _set
