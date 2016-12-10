#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/mkdir.py]

Defines the "mkdir" command.
"""

verbs = {}

def mkdir(env, args, kwargs):
    """[PATH,...]@Create a directory."""
    for arg in args:
        try:
            os.mkdir(env.directory + "/" + arg)
        except OSError:
            pass
    return

verbs["mkdir"] = mkdir
