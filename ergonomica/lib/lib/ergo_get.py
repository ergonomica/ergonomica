#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/get.py]

Defines the "get" command.
"""


def main(args):
    """get: Get the value of a variable.

    Usage:
       get VAR
    """

    return args.ns[args.args['VAR']]
