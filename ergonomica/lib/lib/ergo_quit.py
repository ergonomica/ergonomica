#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_quit.py]

Defines the "quit" command.
"""


def quit(argc):
    """quit: Exit the Ergonomica shell.

    Usage:
       quit
    """

    argc.env.run = False


exports = {'quit': quit}


