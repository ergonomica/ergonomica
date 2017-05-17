#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/set.py]

Defines the "set" command.
"""

import copy

verbs = {}

def _set(argc):
    """VAR VAL@Sets VAR to VAL in namespaced."""
    filtered_ns = copy.copy(argc.ns)
    for item in [x for x in filtered_ns]:
        if callable(filtered_ns[item]):
            del filtered_ns[item]
    argc.ns[argc.args['VAR']] = eval(argc.args['VAL'], filtered_ns)
    return

verbs["set"] = _set
