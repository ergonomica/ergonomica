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
       print <str>STRING [-f INDICES...] [-m MULTIPLIER]

    Options:
       -f --filter     INDICES  Print the items of the input with the specified indices.
       -c --multiplier COUNT    Print the given item COUNT times (seperated by newlines).

    """

    return argc.args['STRING']
