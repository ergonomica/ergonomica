#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/length.py]

Defines the "length" command.
"""


def main(argc):
    """length: Return the number of items in STDIN.

    Usage:
        length
    """    

    return len(argc.stdin)

