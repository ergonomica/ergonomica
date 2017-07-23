#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_equal.py]

Defines the "equal" command.
"""


def main(argc):
    """equal: Compare equality of arguments.

    Usage:
        equal [ARGS...]
    """

    first_element = argc.args['ARGS'][0]
    return argc.args['ARGS'] == [first_element] * len(argc.args['ARGS'])
