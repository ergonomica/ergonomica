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
    for x in args:
        shutil.copy2(env.directory + "/" + x, kwargs["path"])
    return

verbs["copy"] = cp
verbs["cp"] = cp
