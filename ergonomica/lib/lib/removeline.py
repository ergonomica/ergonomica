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
    """[LINENUM,...] {file:file}@Remove lines with indices LINENUM from file."""

    _file = kwargs["file"]
    if _file[0] not in ["/", "~"]:
        _file = os.path.join(env.directory, _file)

    # read lines and delete file
    lines = open(_file, "rb").readlines()
    os.remove(_file)

    # delete line
    for item in args:
        lines[int(item)] = None

    # write to file
    lines = [x for x in lines if x is not None]
    open(kwargs["file"], "w").writelines(lines)

    return

verbs["removeline"] = removeline
