#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""

verbs = {}

def pwd(env, args):
    """@Print the working directory."""
    return env.directory

verbs["pwd"] = pwd
