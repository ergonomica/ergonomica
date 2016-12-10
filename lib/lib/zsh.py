#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/fish.py]

Defines the "fish" command.
"""

from lib.util.util import run_command

verbs = {}

def zsh(env, args, kwargs):
    """[STRING, ...]@Open a ZSH shell. If STRINGs specified, evaluate strings in ZSH."""
    if args == []:
        run_command("zsh")
    else:
        return [run_command('zsh -c "' + x + '"') for x in args]
    return

verbs["zsh"] = zsh
