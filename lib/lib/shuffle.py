#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/shuffle.py]

Defines the "shuffle" command.
"""

import random

verbs = {}

def _shuffle(env, args, kwargs):
    """[VARNAME,...]@Get the value of a variable"""
    random.shuffle(args)
    if "num" not in kwargs:
        return args
    else:
        out = []
        for i in range(int(kwargs["num"])):
            out.append(args[i])
        return out

verbs["shuffle"] = _shuffle
verbs["randomize"] = _shuffle
