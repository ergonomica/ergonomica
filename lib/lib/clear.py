#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

import os

verbs = {}

def clear(env, args, kwargs):
    """@Clears the screen."""
    os.system('clear')

verbs["clear"] = clear
