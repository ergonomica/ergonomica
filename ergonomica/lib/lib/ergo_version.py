#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/version.py]

Defines the "version" command.
"""


def ergo_version(argc):
    """version: Return ergonomica version information.
    
    Usage:
        version
    """
    
    # &&&VERSION&&& replaced by pip install to the current version.
    return "Ergonomica &&&VERSION&&&."
