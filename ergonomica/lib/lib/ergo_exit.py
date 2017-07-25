#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_exit.py]

Defines the "exit" command.
"""


def exit(args):
    """exit: Exit the Ergonomica shell.

    Usage:
       exit
    """

    args.env.run = False

exports = {'exit': exit}
