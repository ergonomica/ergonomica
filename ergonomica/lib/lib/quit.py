#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/quit.py]

Defines the "quit" command.
"""

verbs = {}

def Quit(env, args, kwargs):
    """@Quits the ergonomica shell."""
    env.run = False

verbs["quit"] = Quit
verbs["exit"] = Quit
