#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/removeline.py]

Defines the "removeline" command.
"""

import os

verbs = {}

def removeline(env, args, kwargs):
    """[LINENUM1,LINENUM2,...] {file:filename}@Remove lines with indices LINENUM from file filename. """
    _file = kwargs["file"]
    if _file[0] not in ["/", "~"]:
        _file = os.path.join(env.directory, _file)
    lines = open(_file, "rb").readlines()
    os.remove(_file)
    for item in args:
        lines[int(item)] = None
    lines = [x for x in lines if x is not None]
    open(kwargs["file"],"w").writelines(lines)
    return
    
verbs["removeline"] = removeline
