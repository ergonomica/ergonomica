#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/error_handler.py]

Describe errors.
"""

# pylint doesn't know where this is being imported
# pylint: disable=import-error

import difflib

from lib.lang.parser import tokenize                                           
from lib.load.load_commands import verbs
from lib.lang.operator import get_operator                                      

def print_error_message(BLOCK):
    """Print an error message for a block."""
    tokenized_block = tokenize(BLOCK)
    operator = get_operator(BLOCK)
    if (tokenized_block[0][0] not in verbs) and not operator:
        bad_command = tokenized_block[0][0]
        correction = difflib.get_close_matches(bad_command,verbs.keys(),1,0.75)
        print "[ergo: CommandError]: No such command '%s'." % bad_command
        try:
            print " " * 22 + "Did you mean %s?" % (correction[0])
        except IndexError:
            pass
    else:                                                           
        STDOUT = repr(error)

class ErgonomicaError(Exception):
    """Base class for exceptions in this module."""
    pass
