#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/multiply.py]

Defines the "multiply" command.
"""

from lib.lang.error import ErgonomicaError

verbs = {}

def multiply(env, args, kwargs):
    """[STRING,...] {num:N}@Prints its input N times."""
    try:
        return args * int(kwargs["num"])
    except KeyError:
        raise ErgonomicaError("[ergo: ArgumentError]: No 'num' specified.")

verbs["multiply"] = multiply
verbs["mul"] = multiply
