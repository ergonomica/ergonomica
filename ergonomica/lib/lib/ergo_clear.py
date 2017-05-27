#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

from prompt_toolkit.shortcuts import clear as raw_clear

def ergo_clear(args):
    """clear: Clear the screen.

    Usage:
       clear 
    """
 
    raw_clear()

    return args.env.welcome
