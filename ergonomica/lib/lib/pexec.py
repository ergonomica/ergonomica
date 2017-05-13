#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
[lib/lib/pexec.py]

Defines the "pexec" command.
"""

verbs = {}

def pexec(argc):
    """STRING@"""
    globals().update(argc.ns)
    globals()['stdin'] = argc.stdin
    return eval(argc.args['STRING'], globals())

verbs["pexec"] = pexec
