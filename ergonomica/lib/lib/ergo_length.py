#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/length.py]

Defines the "length" command.
"""


def ergo_length(argc):
    """length: Return the number of items in STDIN.

    Usage:
        length
    """    

    return len(argc.stdin)

