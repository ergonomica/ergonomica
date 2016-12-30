#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

# Needs this for documentation purposes
# pylint: disable=line-too-long

"""
[lib/lib/addline.py]

Defines the "addline" command.
"""

import os
from lib.lang.error import ErgonomicaError

verbs = {}

def addline(env, args, kwargs):
    """[LINE,...] {file:filename}@Adds all LINEs to file filename. Note that newlines must be included."""
    try:
        _file = kwargs["file"]
        if _file[0] not in ["/", "~"]:
            _file = os.path.join(env.directory, _file)
        for line in args:
            open(kwargs["file"], "a").write(line)
        return
    except KeyError:
        raise ErgonomicaError("[ergo: ArgumentError]: No file set for addline.")

verbs["addline"] = addline
verbs["append"] = addline
