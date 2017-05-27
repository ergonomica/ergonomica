#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/get.py]

Defines the "get" command.
"""


def ergo_get(args):
    """get: Get the value of a variable.

    Usage:
       get VAR
    """

    return args.ns[args.args['VAR']]

