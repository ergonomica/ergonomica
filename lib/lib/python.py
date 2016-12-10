#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/python.py]

Defines the "python" command.
"""

verbs = {}

def python(env, args, kwargs):
    """@Drop into a python REPL."""
    temp_space = {}
    try:
        temp_space = globals()
        temp_space.update({"exit":sys.exit})
        temp_space.update({"quit":sys.exit})
        temp_space.update(env.namespace)
        code.InteractiveConsole(locals=temp_space).interact()
    except SystemExit:
        for key in temp_space:
            env.namespace[key] = temp_space[key]
        return ""

verbs["python"] = python
