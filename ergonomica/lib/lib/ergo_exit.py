#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_exit.py]

Defines the "exit" command.
"""


def exit(argc):
    """exit: Exit the Ergonomica shell.

    Usage:
       exit
    """

    argc.env.run = False

exports = {'exit': exit}


