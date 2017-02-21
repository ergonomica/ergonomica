#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/echo.py]

Defines the "echo"/"print" command.
"""

from lib.lang.error import ErgonomicaError

verbs = {}

def echo(env, args, kwargs):
    """[STRING,...] {ind:[INT,...]}@Prints its input. If ind specified, returns the items of its input with the specified indices."""
    try:
        return [args[i] for i in kwargs["ind"]]
    except KeyError:
            return args
    except IndexError:
            raise ErgonomicaError("[ergo: ArgumentError]: Indices passed not valid for passed list.")

verbs["echo"] = echo
verbs["print"] = echo
