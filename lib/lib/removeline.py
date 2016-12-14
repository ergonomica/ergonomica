#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/find.py]

Defines the "find" command.
"""

import os
import fnmatch

verbs = {}

def removeline(env, args, kwargs):
    """[DIR] {name:PATTERN}@Finds a file with a pattern."""
    _file = kwargs["file"]
    if _file[0] not in ["/", "~"]:
        _file = os.path.join(env.directory, _file)
    lines = open(_file, "rb").readlines()
    os.remove(_file)
    for item in args:
        del lines[int(item)]
    open(kwargs["file"],"w").writelines(lines)
    return
    
verbs["removeline"] = removeline
