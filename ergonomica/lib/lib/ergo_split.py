#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_split.py]

Defines the "split" command.
"""


def split(argc):
    """split: Split a string.

    Usage:
        split STRING SEP
    """

    return argc.args['STRING'].split(argc.args['SEP'])


exports = {'split': split}
