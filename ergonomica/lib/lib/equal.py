#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/equal.py]

Defines the "equal" command.
"""

verbs = {}

def equal(argc):
    """equal: Compare if arguments are not equal.
    
    Usage: 
       equal A B
    """
    
    return argc.args['A'] == argc.args['B']

verbs["equal"] = equal
