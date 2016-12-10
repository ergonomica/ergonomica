#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/whoami.py]

Defines the "whoami" command.
"""

verbs = {}

def whoami(env, args, kwargs):
    """@Return the user."""
    return env.user

verbs["whoami"] = whoami
