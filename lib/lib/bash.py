#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

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
        os.system(parsed_env + " bash")
        #os.system("bash")
    else:
        return map(run_command, [parsed_env + " " + x for x in args])
    return ""

verbs["bash"] = bash
verbs["b"] = bash
