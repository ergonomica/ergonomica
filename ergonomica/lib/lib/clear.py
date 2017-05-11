#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

from prompt_toolkit.shortcuts import clear as raw_clear

verbs = {}

def clear(args):
    """@Clears the screen."""

    raw_clear()

    return args.env.welcome
        
verbs["clear"] = clear
