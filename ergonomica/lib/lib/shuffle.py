#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/shuffle.py]

Defines the "shuffle" command.
"""

import random

verbs = {}

def _shuffle(env, args):
    """[STRING,...]@Shuffle all input."""
    random.shuffle(args)
    return args

verbs["shuffle"] = _shuffle
