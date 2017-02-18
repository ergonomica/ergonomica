#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/shuffle.py]

Defines the "shuffle" command.
"""

import random

verbs = {}

def _shuffle(env, args, kwargs):
    """[STRING,...]@Shuffle all input."""
    random.shuffle(args)
    return args

verbs["shuffle"] = _shuffle
