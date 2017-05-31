#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/mkdir.py]

Defines the "mkdir" command.
"""

import os


def main(argc):
    """mkdir: Make a directory.

    Usage:
       mkdir DIR
    """

    os.mkdir(os.path.expanduser(argc.args['DIR']))
