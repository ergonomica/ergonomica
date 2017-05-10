#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/quit.py]

Defines the "quit" command.
"""

verbs = {}

def _quit(env, args):
    """@Quits the ergonomica shell."""
    env.run = False

verbs["quit"] = _quit

