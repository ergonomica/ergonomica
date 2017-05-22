#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""

from ergonomica.lib.lang.error import ErgonomicaError

verbs = {}

def whoami(argc):
    """whoami: Return the current user.

    Usage:
       whoami
    """
    
    return argc.env.user
    
verbs["whoami"] = whoami
