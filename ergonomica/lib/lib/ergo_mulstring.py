#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_mulstring.py]

Defines the "mulstring" command.
"""


def mul(argc):
    """mulstring: Multiply a string N times.

    Usage:
        mulstring STRING N
    """
    
    yield int(argc.args['N']) * argc.args['STRING']


exports = {'mulstring': mul}