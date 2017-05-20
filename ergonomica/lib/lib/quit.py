#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/quit.py]

Defines the "quit" command.
"""

verbs = {}

def _quit(args):
    """quit: Exit the Ergonomica shell.

    Usage:
       quit
    """

    args.env.run = False

verbs["quit"] = _quit
