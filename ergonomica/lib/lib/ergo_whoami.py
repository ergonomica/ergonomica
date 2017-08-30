#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""


def whoami(argc):
    """whoami: Return the current user.

    Usage:
       whoami
    """

    return argc.env.user


exports = {'whoami': whoami}


