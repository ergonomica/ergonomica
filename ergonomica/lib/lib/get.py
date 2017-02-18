#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/get.py]

Defines the "get" command.
"""

verbs = {}

def get(env, args, kwargs):
    """[VARNAME,...]@Get the value of a variable"""
    return [env.namespace[x] for x in args]

verbs["get"] = get
verbs["val"] = get
