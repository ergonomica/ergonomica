#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/python.py]

Defines the "python" command.
"""

import sys
import code

verbs = {}

def python(env, args, kwargs):
    """@Drop into a python REPL."""
    temp_space = globals()
    if args != []:
        # for some reason exec is a statement
        for arg in args:
            exec(arg, temp_space)
    else:
        try:
            temp_space = globals()
            temp_space.update({"exit":sys.exit})
            temp_space.update({"quit":sys.exit})
            temp_space.update(env.namespace)
            code.InteractiveConsole(locals=temp_space)
        except SystemExit:
            pass
    
    for key in temp_space:
        env.namespace[key] = temp_space[key]
    return ""

verbs["python"] = python
