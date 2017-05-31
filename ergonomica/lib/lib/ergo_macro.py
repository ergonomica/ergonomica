#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/macro.py]

Defines the "macro" command.
"""


def main(argc):
    """macro: Defines a text macro mapping STRING to REPLACEMENT_STRING.

    Usage:
        macro STRING REPLACEMENT_STRING
    """

    argc.env.macros[argc.args['STRING']] = argc.args['REPLACEMENT_STRING']
