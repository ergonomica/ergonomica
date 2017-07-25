#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_unique.py]

Defines the "unique" command.
"""

def unique(argc):
    """unique: Remove all duplicate elements in input.

    Usage:
        unique
    """
    
    stdout = []

    for i in argc.stdin:
        if i not in stdout:
            stdout.append(i)
    
    return stdout
    

exports = {'unique': unique}
