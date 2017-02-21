#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""

from lib.lang.error import ErgonomicaError

verbs = {}

def whoami(env, args, kwargs):
    """@Return the user."""
    if (args, kwargs) != ([], {}):
        raise ErgonomicaError("[ergo: ArgumentError]: Arguments passed to 'whoami' (no arguments should be passed).")
    return env.user

verbs["whoami"] = whoami
