#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/bash.py]

Defines the "bash" command.
"""

from lib.util.util import run_command

verbs = {}

def bash(env, args, kwargs):
    """[STRING,...]@Open a Bash shell. If STRINGs specified, evaluate strings in Bash."""
    if args == []:
        run_command("bash")
        #os.system("bash")
    else:
        return map(run_command, args)
    return

verbs["bash"] = bash
