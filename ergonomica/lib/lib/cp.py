#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/cp.py]

Defines the "cp"/"copy" command.
"""

import shutil

verbs = {}

def cp(env, args):
    """[FILE,NEWPATH,...] [{dest:DEST}]@Copy files. If dest specified, moves all arguments to DEST (not doing one-off)."""
    if "dest" not in kwargs:
        for i in range(0, len(args) - 1):
            try:
                shutil.copy2(env.directory + "/" + args[i], env.directory + "/" + args[i+1])
            except OSError:
                pass
    else:
        for i in args:
            shutil.move(env.directory + "/" + args[i], kwargs["dest"])                
    return

verbs["cp"] = cp
