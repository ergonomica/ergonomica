#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""


def ergo_pwd(args):
    """pwd: Print the working directory.

    Usage:
        pwd
    """
    
    return args.env.directory
