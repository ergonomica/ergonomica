#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

import subprocess
from prompt_toolkit.shortcuts import clear as raw_clear

verbs = {}

def clear(env, args, kwargs):
    """@Clears the screen."""

    raw_clear()

    return env.welcome
        
verbs["clear"] = clear
