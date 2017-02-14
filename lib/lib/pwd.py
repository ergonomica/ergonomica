#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/pwd.py]

Defines the "pwd" command.
"""

verbs = {}

def pwd(env, args, kwargs):
    """@Print the working directory."""
    return env.directory

verbs["pwd"] = pwd
