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
       print <string>STRING... [-m MULTIPLIER] [-f INDICES...]

    Options:
       -f --filter     INDICES  Print the items of the input with the specified indices.
       -m --multiplier MULTIPLIER    Print the given item COUNT times (seperated by newlines).

    """

    if argc.args['--multiplier']:
        return [argc.args['STRING']] * int(argc.args['--multiplier'])
    return argc.args['STRING']
