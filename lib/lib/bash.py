#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/bash.py]

Defines the "bash" command.
"""

import os

verbs = {}

def bash(env, args, kwargs):
    """[STRING,...]@Open a Bash shell. If STRINGs specified, evaluate strings in Bash."""
    if args == []:
        os.system("bash")
    else:
        map(os.system, args)
    return

verbs["bash"] = bash
