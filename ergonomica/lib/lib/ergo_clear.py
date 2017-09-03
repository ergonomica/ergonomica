#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

from prompt_toolkit.shortcuts import clear as raw_clear

def clear(argc):
    """clear: Clear the screen.
    
    Usage:
        clear [-w | --welcome]
    """

    raw_clear()

    if argc.args['--welcome'] or argc.args['-w']:
        print(argc.env.welcome)


exports = {'clear': clear}


