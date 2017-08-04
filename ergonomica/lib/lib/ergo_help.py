#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_help.py]

Defines the "help" command.
"""

def _help(argc):
    """
    help: the Ergonomica help system.
    
    Usage:
        help commands
    """
    
    if argc.args['commands']:
        return [x for x in argc.ns if callable(argc.ns[x])]


exports = {'help': _help}
