#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/cp.py]

Defines the "cp"/"copy" command.
"""

import shutil

verbs = {}

def cp(env, args, kwargs):
    """[FILE,NEWPATH,...]@Copy files."""
    for i in range(0, len(args) - 1):
        try:
            shutil.copy2(env.directory + "/" + args[i], env.directory + "/" + args[i+1])
        except OSError:
            pass
    return
    
verbs["copy"] = cp
verbs["cp"] = cp
