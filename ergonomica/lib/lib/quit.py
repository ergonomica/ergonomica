#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/quit.py]

Defines the "quit" command.
"""

verbs = {}

def _quit(args):
    """@Quits the ergonomica shell."""
    args.env.run = False

verbs["quit"] = _quit

