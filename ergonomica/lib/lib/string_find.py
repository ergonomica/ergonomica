#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/string_find.py]

Defines the "string_find" command.
"""

import os
import fnmatch
import re

verbs = {}

def string_find(env, args, kwargs):
    """[DIR=.] {name:PATTERN=*}@Finds all lines in files in DIR (recursively) that match PATTERN."""
    try:
        pattern = kwargs["name"]
    except KeyError:
        pattern = "*"
    try:
        path = args[0]
    except IndexError:
        path = env.directory
    result = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if fnmatch.fnmatch(os.path.join(root, dir), pattern):
                result.append(os.path.join(root, dir))
        for name in files:
            opened_file = open(os.path.join(root, name), "r").readlines()
            for x in range(len(opened_file)):
                if pattern in opened_file[x]:
                    head = os.path.join(root, name) + ", line %s \n" % x
                    match = re.findall(pattern, opened_file[x])[0]
                    matched_line = opened_file[x].replace(match, env.theme["match"] + match + env.default_color)
                    result.append(head + matched_line)
    return list(set(result))

verbs["string_find"] = string_find
verbs["sfind"] = string_find
