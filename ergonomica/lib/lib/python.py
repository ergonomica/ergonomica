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
[lib/lib/python.py]

Defines the "python" command.
"""

import sys
import os
import shutil

try:
    from ptpython.repl import embed
except ImportError:
    print("[ergo: DependencyError]: PTPython not found. Please pip install ptpython.")

verbs = {}

def python(env, args, kwargs):
    """[STRING,...]@Drop into a python REPL. If STRINGs specified, execute them in Python."""
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

            _vi_mode = False
            if env.EDITOR in ["vi", "vim"]:
                _vi_mode = True


            embed(globals(), temp_space, vi_mode=_vi_mode)
        except SystemExit:
            pass

    for key in temp_space:
        env.namespace[key] = temp_space[key]
    return ""

verbs["python"] = python
