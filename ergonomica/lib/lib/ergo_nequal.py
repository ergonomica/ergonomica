#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/nequal.py]

Defines the "nequal" command.
"""


def ergo_nequal(argc):
    """nequal: Compare if arguments are not equal.
    
    Usage: 
       nequal A B
    """
    
    return argc.args['A'] != argc.args['B']
