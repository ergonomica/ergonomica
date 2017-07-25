#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/get.py]

Defines the "get" command.
"""


def get(args):
    """get: Get the value of a variable.

    Usage:
       get <variable>VAR
    """

    try:
        return args.ns[args.args['VAR']]
    except KeyError:
        print("[ergo: NameError]: No such variable '%s'." % (args.args["VAR"]))


exports = {'get': get}
