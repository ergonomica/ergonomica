#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

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
                os.mkdir(os.path.join(ENV.directory, directory))
        except OSError:
            if ("overwrite" in kwargs) and (kwargs["overwrite"] == 'true'): 
                pass
            else:
                raise OSError

verbs["mkdir"] = mkdir
