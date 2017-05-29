#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_quit.py]

Defines the "quit" command.
"""


def main(args):
    """quit: Exit the Ergonomica shell.

    Usage:
       quit
    """

    args.env.run = False
