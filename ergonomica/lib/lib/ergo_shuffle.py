#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_shuffle.py]

Defines the "shuffle" command.
"""

import random


def shuffle(argc):
    """
    shuffle: Shuffle STDIN.

    Usage:
        shuffle
    """

    random.shuffle(argc.stdin)
    return argc.stdin


exports = {'shuffle': shuffle}