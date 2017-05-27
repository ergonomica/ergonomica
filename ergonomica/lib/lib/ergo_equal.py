#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_equal.py]

Defines the "equal" command.
"""


def ergo_equal(argc):
    """equal: Compare if arguments are not equal.
    
    Usage: 
       equal A B
    """
    
    return argc.args['A'] == argc.args['B']
