#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/version.py]

Defines the "version" command.
"""

verbs = {}

def version(env, args, kwargs):
    """@Return ergonomica version information."""
    # &&&VERSION&&& replaced by Homebrew to the current version.
    return "Ergonomica &&&VERSION&&&."

verbs["version"] = version
