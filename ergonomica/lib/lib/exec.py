#!/usr/bin/python
# -*- coding: utf-8 -*-

"""                                                                            [lib/lib/exec.py]

Defines the "exec" command.
"""

verbs = {}

def _exec(argc):
    """STRING@"""
    globals().update(argc.ns)
    globals()['stdin'] = argc.stdin
    return eval(argc.args['STRING'], globals())

verbs["exec"] = _exec
