#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_read.py]

Defines the "read" command.
"""

from ergonomica.lib.util.util import expand_path

def read(argc):
    """
    read: Read a file.

    Usage:
       read FILE
    """

    try:
        return open(expand_path(argc.env, argc.args['FILE']), "r").read().split("\n")
    except IOError:
        print("[ergo: IOError]: No such readable file '%s'." % (argc.args['FILE']))


exports = {'read': read}
