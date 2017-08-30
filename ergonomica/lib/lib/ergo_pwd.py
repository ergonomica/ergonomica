#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""


def pwd(argc):
    """pwd: Print the working directory.

    Usage:
        pwd
    """

    return argc.env.directory


exports = {'pwd': pwd}


