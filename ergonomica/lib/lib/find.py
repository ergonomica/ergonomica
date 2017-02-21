#!/usr/bin/python
# -*- coding: utf-8 -*-

# required for documentation
# pylint: disable=line-too-long

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

"""
[lib/lib/find.py]

Defines the "find" command.
"""

import os
import fnmatch
from lib.lang.error import ErgonomicaError

verbs = {}

def find(env, args, kwargs):
    """[DIR] {name:PATTERN}@Finds a file with name matching PATTERN. If no DIR specified, chooses current directory."""
    try:
        pattern = kwargs["name"]
    except KeyError:
        pattern = "*"
    try:
        path = args[0]
    except IndexError:
        path = env.directory

    if not os.path.isdir(path):
        raise ErgonomicaError("[ergo: NoSuchDirectoryError]: No such directory '%s'." % (path))

    result = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if fnmatch.fnmatch(os.path.join(root, dir), pattern):
                result.append(os.path.join(root, dir))
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return [env.theme["files"] + x for x in list(set(result))]

verbs["find"] = find
