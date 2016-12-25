#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/bash.py]

Lexer module. Contains tokenize().
"""

# pylint doesn't know that `from lib.lib...` is run from the above dir
# pylint: disable=import-error

import re
from lib.util.util import run_command

def run_bash(stdin, pipe):
    try:
        print(stdin)
        print(run_command(stdin))
        pipe.setstack_args(run_command(stdin))
        return pipe.getstack_args(-1)
    except OSError:
        pass
