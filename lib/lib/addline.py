#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/addline.py]

Defines the "addline" command.
"""

import os

verbs = {}

def addline(env, args, kwargs):
    """[STRING,...]@Adds a line to a file."""
    _file = kwargs["file"]
    if _file[0] not in ["/", "~"]:
        _file = os.path.join(env.directory, _file)
    for line in args:
        open(kwargs["file"],"a").write(line)
    return

verbs["addline"] = addline
verbs["append"] = addline
