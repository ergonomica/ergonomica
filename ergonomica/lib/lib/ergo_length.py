#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/length.py]

Defines the "length" command.
"""


def length(argc):
    """length: Return the number of items in STDIN.

    Usage:
        length
        length STRING
    """
    
    if argc.args['STRING']:
        return len(argc.args['STRING'])
    else:
        return len(argc.stdin)


exports = {'length': length}
