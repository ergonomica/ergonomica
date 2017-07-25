#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/mul.py]

Defines the "mul" command.
"""


def mul(argc):
    """mul: Multiply a string N times.

    Usage:
        mul STRING N
    """
    
    yield int(argc.args['N']) * argc.args['STRING']


exports = {'mul': mul}