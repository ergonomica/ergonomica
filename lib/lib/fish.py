#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/fish.py]

Defines the "fish" command.
"""

import os

verbs = {}

def fish(env, args, kwargs):
    """[STRING,...]@Open a Fish shell. If STRINGs specified, evaluate strings in Fish."""
    if args == []:
        os.system("bash")
    else:
        map(os.system, args)
    return

verbs["fish"] = fish
