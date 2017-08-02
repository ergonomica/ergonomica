#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_split.py]

Defines the "split" command.
"""


def split(argc):
    """split: Split a string.

    Usage:
        split STRING [SEP]
    """

    if argc.args['SEP']:
        return argc.args['STRING'].split(argc.args['SEP'])
    else:
        return list(argc.args['STRING'])


exports = {'split': split}
