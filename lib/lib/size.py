#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/size.py]

Defines the "size" command.
"""

import os

verbs = {}

def size(env, args, kwargs):
    """[STRING,...]@Prints its input."""
    out = []
    for item in args:
        if item[0] in ["/", "~"]:
            out.append("%s bytes" % os.path.getsize(item))
        else:
            out.append("%s bytes" % os.path.getsize(env.directory + "/" + item))
    return out

verbs["size"] = size
