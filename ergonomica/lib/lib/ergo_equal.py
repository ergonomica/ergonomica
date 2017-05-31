#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_equal.py]

Defines the "equal" command.
"""


def main(argc):
    """equal: Compare equality of arguments.

    Usage:
        equal A B
    """

    return argc.args['A'] == argc.args['B']
