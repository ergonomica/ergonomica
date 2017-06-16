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

    try:
        return args.ns[args.args['VAR']]
    except KeyError:
        print("[ergo: NameError]: No such variable '%s'." % (args.args["VAR"]))
