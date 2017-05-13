#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/read.py]

Defines the "read" command.
"""

from __future__ import print_function

verbs = {}

def read(args):
    """FILE@Read all lines of FILE."""
    try:
        open(args['FILE'], "r").read().split("\n")
    except IOError:
        print("[ergo: IOError]: No such readable file '%s'." % (args['FILE']))

verbs["read"] = read

