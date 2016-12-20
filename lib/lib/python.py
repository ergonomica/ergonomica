#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/python.py]

Defines the "python" command.
"""

import sys
import os
import shutil
from ptpython.repl import embed

verbs = {}

def python(env, args, kwargs):
    """@Drop into a python REPL."""
    temp_space = globals()
    if args != []:
        # for some reason exec is a statement
        for arg in args:
            exec(arg, temp_space)
            return ""
    else:
        try:
            temp_space = globals()
            temp_space.update({"exit":sys.exit})
            temp_space.update({"quit":sys.exit})
            temp_space.update(env.namespace)
            temp_space.update({"shutil":shutil})
            temp_space.update({"os":os})
            temp_space.update({"ergo":env.ergo})
            #code.InteractiveConsole(locals=temp_space)
            embed(globals(), temp_space)
        except SystemExit:
            pass
    
    for key in temp_space:
        env.namespace[key] = temp_space[key]
    return ""

verbs["python"] = python
