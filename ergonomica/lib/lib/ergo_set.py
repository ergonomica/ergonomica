#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_set.py]

Defines the "set" command.
"""

import copy


def main(argc):
    """set: Set variables.
    Usage:
       set VAR VAL
    """
    filtered_ns = copy.copy(argc.ns)
    for item in [x for x in filtered_ns]:
        if callable(filtered_ns[item]):
            del filtered_ns[item]
    try:
        argc.ns[argc.args['VAR']] = eval(argc.args['VAL'], filtered_ns)
    except:
        argc.ns[argc.args['VAR']] = argc.args['VAL']
    return
