#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_cd.py]

Defines the "cd" command.
"""

import sys
import os
from ergonomica import ErgonomicaError
from ergonomica.lib.util.util import expand_path

try:
    input = raw_input
except NameError:
    pass

def _input(argc):
    """input: Get input from the user.

    Usage:
        input PROMPT
    """

    return input(argc.args['PROMPT'])


exports = {'input': _input}
