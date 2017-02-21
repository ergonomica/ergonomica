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
import traceback

from lib.lang.parser import tokenize
from lib.load.load_commands import verbs
from lib.lang.operator import get_operator
from lib.lang.operator import operators
from lib.lang.error import ErgonomicaError

def get_error_message(BLOCK):
    """Print an error message for a block."""
    tokenized_block = tokenize(BLOCK)
    operator = get_operator(BLOCK)    
    if get_operator(BLOCK) and get_operator(BLOCK) not in operators:
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

def handle_runtime_error(block, error):
    """Handle ergonomica errors."""
    # if no ergonomica error message can be generated
    if isinstance(error, ErgonomicaError):
        raise error
    if not get_error_message(block):
        # fallback to python
        return traceback.format_exc()
    else:
        return get_error_message(block)
