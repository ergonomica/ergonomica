#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/fish.py]

Defines the "fish" command.
"""

import os
from lib.util.util import run_command

verbs = {}

def fish(env, args, kwargs):
    """[STRING,...]@Open a Fish shell. If STRINGs specified, evaluate strings in Fish."""
    if args == []:
        os.environ["PATH"] = env.PATH
        os.system("fish")
    else:
        return [run_command(env, 'fish -c "' + x + '"') for x in args]
    return

verbs["fish"] = fish
