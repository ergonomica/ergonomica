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
       set <variable>VAR VAL
    """

    filtered_ns = copy.copy(argc.ns)
    for item in [x for x in filtered_ns]:
        if callable(filtered_ns[item]):
            del filtered_ns[item]
    try:
        # Ergonomica's purpose is literally to evaluate arbitrary code
        # pylint: disable=eval-used
        argc.ns[argc.args['VAR']] = eval(argc.args['VAL'], filtered_ns)
    # this is the way it's supposed to work
    # pylint: disable=broad-except
    except Exception:
        argc.ns[argc.args['VAR']] = argc.args['VAL']
    return
