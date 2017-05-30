#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""


def main(argc):
    """pwd: Print the working directory.

    Usage:
        pwd
    """
    
    return argc.env.directory
