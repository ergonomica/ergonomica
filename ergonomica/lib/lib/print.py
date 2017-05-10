#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/print.py]

Defines the "echo"/"print" command.
"""

# from ergonomica.lib.lang.error import ErgonomicaError

verbs = {}

def _print(_env, _ns, _args):
    """<string>@Prints its input. If ind specified, returns the items of its input with the specified indices."""
    return _args['<string>']

verbs["print"] = _print
