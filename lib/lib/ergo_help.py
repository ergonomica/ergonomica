#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/ergo_help.py]

Defines the "ergo_help" command.
"""

import os

verbs = {}

def ergo_help(env, args, kwargs):
    """[COMMAND,...]@Ergonomica help"""
    out = ""
    if args == []:
        pruned_verbs = {}
        for item in env.verbs:
            if item not in pruned_verbs:
                pruned_verbs[item] = env.verbs[item]
        for item in pruned_verbs:
            docstring = env.verbs[item].__doc__.split("@")
            out += "%-26s |  %29s\n" % (item + " " + docstring[0], docstring[1])
    else:
        for item in args:
            out += env.verbs[item].__doc__ + "\n"
    return out

verbs["help"] = ergo_help
