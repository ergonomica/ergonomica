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
[lib/lib/bash.py]

Defines the "bash" command.
"""

import os
from lib.util.util import run_command

verbs = {}

def bash(env, args, kwargs):
    """[STRING,...]@Open a Bash shell. If STRINGs specified, evaluate strings in Bash."""
    parsed_env = " ".join(["env %s=%s" % (k, env.namespace[k]) for k in env.namespace])
    if args == []:
        os.environ["PATH"] = env.PATH
        os.system(parsed_env + " bash")
    else:
        return [item for sublist in [run_command(env, x).split("\n") for x in [parsed_env + " " + x for x in args]] for item in sublist]
    return ""

verbs["bash"] = bash
verbs["b"] = bash
