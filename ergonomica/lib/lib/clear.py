#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

from prompt_toolkit.shortcuts import clear as raw_clear

verbs = {}

def clear(args):
    """clear: Clear the screen.

    Usage:
       clear [-n | --no-welcome]
    
    Options:
       -n --no-welcome  Do not show the welcome message.
    """

    raw_clear()

    return args.env.welcome
        
verbs["clear"] = clear
