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
[lib/lib/mkdir.py]

Defines the "mkdir" command.
"""

import os

verbs = {}

def mkdir(env, args, kwargs):
    """[DIR,...]@Make DIRs."""
    for directory in args:
        try:
            if directory[0] in ["/", "~"]:
                os.mkdir(directory)
            else:
                os.mkdir(os.path.join(env.directory, directory))
        except OSError:
            if ("overwrite" in kwargs) and (kwargs["overwrite"] == 'true'):
                pass
            else:
                raise OSError

verbs["mkdir"] = mkdir
