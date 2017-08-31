#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        input [PROMPT]
    """
    
    prompt = argc.args['PROMPT'] if argc.args['PROMPT'] else '[ergo: input]: '

    return input(prompt)


exports = {'input': _input}


