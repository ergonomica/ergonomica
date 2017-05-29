#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""


def ergo_whoami(argc):
    """whoami: Return the current user.

    Usage:
       whoami
    """
    
    return argc.env.user
