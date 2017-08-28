#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_trim.py]

Defines the "trim" command.
"""

def trim(argc):
    """trim: Trim surrounding whitespace.

    Usage:
        trim [head|tail] STRING
    """
    
    if argc.args['head']:
        return argc.args['STRING'].lstrip()
    
    if argc.args['tail']:
        return argc.args['STRING'].rstrip()
    
    else:
        return argc.args['STRING'].strip()
    

exports = {'trim': trim}
