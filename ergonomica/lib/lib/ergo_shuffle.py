#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_shuffle.py]

Defines the "shuffle" command.
"""

import random

def main(argc):
    """
    shuffle: Shuffle STDIN.

    Usage:
        shuffle
    """

    random.shuffle(argc.stdin)
    return argc.stdin
