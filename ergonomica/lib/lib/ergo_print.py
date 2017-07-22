#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_print.py]

Defines the "print" command.
"""


def main(argc):
    """
    print: Print strings.

    Usage:
       print <string>[STRINGS...] [-m MULTIPLIER]

    Options:
       -m --multiplier MULTIPLIER    Print the given item COUNT times (seperated by newlines).
    """
    
    print(argc.args['INDICES'])
    
    if argc.args['--multiplier']:
        return argc.args['STRINGS'] * int(argc.args['--multiplier'])
    return argc.args['STRINGS']
