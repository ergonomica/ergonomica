#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/nequal.py]

Defines the "nequal" command.
"""

verbs = {}

def nequal(argc):
    """A B@Returns A != B."""
    return argc.args['A'] != argc.args['B']

verbs["nequal"] = nequal
