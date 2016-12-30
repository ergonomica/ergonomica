#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/ergo_help.py]

Defines the "ergo_help" command.
"""

verbs = {}

def ergo_help(env, args, kwargs):
    """[COMMAND,...]@Display all ergonomica commands. If COMMANDs specified, returns the docstrings and arguments for them."""
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
            docstring = env.verbs[item].__doc__.split("@")
            out += "%-26s |  %29s\n" % (item + " " + docstring[0], docstring[1])
    return out

verbs["help"] = ergo_help
