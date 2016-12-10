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

def zsh(env, args, kwargs):
    """[STRING, ...]@Open a ZSH shell. If STRINGs specified, evaluate strings in ZSH."""
    if args == []:
        os.system("zsh")
    else:
        map(os.system, args)
    return

verbs["zsh"] = zsh
