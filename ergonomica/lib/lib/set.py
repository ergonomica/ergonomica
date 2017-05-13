#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/set.py]

Defines the "set" command.
"""

verbs = {}

def _set(args):
    """VAR VAL@Sets VAR to VAL in namespaced."""
    args.ns[args.args['VAR']] = args.args['VAL']
    return

verbs["set"] = _set
