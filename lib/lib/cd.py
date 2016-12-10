#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/cd.py]

Defines the "cd" command.
"""

import os

verbs = {}

def cd(env, args, kwargs):
    """DIR@Changes to a directory."""
    try:
        if args[0][0] in ["~", "/"]:
            os.chdir(args[0])
        else:
            os.chdir(env.directory + "/" + args[0])
        env.directory = os.getcwd()
    except OSError:
        raise ErgonomicaError("[ergo: NoSuchDirectoryError]: no such directory '%s'.")

verbs["cd"] = cd
verbs["directory"] = cd
