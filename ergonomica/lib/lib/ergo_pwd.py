#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""

verbs = {}

def pwd(args):
    """@Print the working directory."""
    return args.env.directory

verbs["pwd"] = pwd
