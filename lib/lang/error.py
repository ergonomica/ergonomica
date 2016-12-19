#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/error.py]

Define the ErgonomicaError exception class.
"""

import traceback
from lib.lang.error_handler import get_error_message

class ErgonomicaError(Exception):
    """Base class for exceptions in this module."""
    pass

def handle_runtime_error(block, error):
    # if no ergonomica error message can be generated
    if isinstance(error, ErgonomicaError):
        raise ErgonomicaError
    if not get_error_message(block):
        # fallback to python
        return [traceback.format_exc()]
    else:
        return get_error_message(block)
