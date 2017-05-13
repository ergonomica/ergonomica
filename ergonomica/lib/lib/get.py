#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/get.py]

Defines the "get" command.
"""

verbs = {}

def _get(args):
    """VAR@Gets the value of VAR in namespace."""
    return args.ns[args.args['VAR']]

verbs["get"] = _get
