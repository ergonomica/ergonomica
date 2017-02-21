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
[lib/lib/alias.py]

Defines the "alias" command.
"""

from lib.lang.error import ErgonomicaError

verbs = {}

def alias(env, args, kwargs):
    """ALIASNAME COMMAND@Create alias ALIASNAME for COMMAND."""
    try:
        env.verbs[args[0]] = env.verbs[args[1]]
    except IndexError:
        raise ErgonomicaError("[ergo: ArgumentError]: Please specify two arguments for 'ALIAS': ALIASNAME and COMMANDNAME")
    except KeyError:
        raise ErgonomicaError("[ergo: CommandError]: No such command '' for 'ALIAS'." % (args[1]))

verbs["alias"] = alias
