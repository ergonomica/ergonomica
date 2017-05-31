#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

from prompt_toolkit.shortcuts import clear as raw_clear

def main(argc):
    """clear: Clear the screen.

    Usage:
       clear
    """

    raw_clear()

    return [argc.env.welcome]
