#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/mv.py]

Defines the "mv" command.
"""

import shutil

verbs = {}

def mv(env, args, kwargs):
    """[FILE,NEWPATH,...]@Move files."""
    for i in range(0, len(args) - 1):
        try:
            shutil.move(env.directory + "/" + args[i], env.directory + "/" + args[i+1])
        except OSError:
            pass
    return

verbs["move"] = mv
verbs["mv"] = mv
