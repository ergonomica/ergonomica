#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

import subprocess

verbs = {}

def clear(env, args, kwargs):
    """@Clears the screen."""

    # TODO: see if there's a more portable method of clearing the screen

    try:

        # linux/bsd (BASH)
        subprocess.call("clear", shell=True)

    except OSError:
        
        # windows
        subprocess.call("cls", shell=True)

verbs["clear"] = clear
