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

def weather(env, args, kwargs):
    """[STRING,...]@Open a Bash shell. If STRINGs specified, evaluate strings in Bash."""
    return [run_command("curl -s wttr.in/%s" % (x.strip().lower())) for x in args]

verbs["weather"] = weather
