#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/fish.py]

Defines the "fish" command.
"""

import os
from lib.util.util import run_command

verbs = {}

def zsh(env, args, kwargs):
    """[STRING, ...]@Open a ZSH shell. If STRINGs specified, evaluates strings in ZSH."""
    if args == []:
        os.environ["PATH"] = env.PATH
        os.system("zsh")
    else:
        return [run_command(env, 'zsh -c "' + x + '"') for x in args]
    return

verbs["zsh"] = zsh
