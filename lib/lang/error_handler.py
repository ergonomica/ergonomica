#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/error_handler.py]

Describe errors.
"""

# pylint doesn't know where this is being imported
# pylint: disable=import-error

# BLOCK is the name standard used in ergonomica, should be used here
# pylint: disable=invalid-name

import difflib

from lib.lang.parser import tokenize
from lib.load.load_commands import verbs
from lib.lang.operator import get_operator

def get_error_message(BLOCK):
    """Print an error message for a block."""
    tokenized_block = tokenize(BLOCK)
    operator = get_operator(BLOCK)    
    if get_operator(BLOCK):
        return "[ergo: OperatorError]: No such operator '%s'." % get_operator(BLOCK)
    elif (tokenized_block[0][0] not in verbs) and not operator:
        bad_command = tokenized_block[0][0]
        correction = difflib.get_close_matches(bad_command, verbs.keys(), 1, 0.55)
        s = "[ergo: CommandError]: No such command '%s'." % bad_command
        try:
            return s + "\n" + " " * 22 + "Did you mean %s?" % (correction[0])
        except IndexError:
            return s
    # when this command is called, this means that its passed through all operators
    else:
        return False
    return True
