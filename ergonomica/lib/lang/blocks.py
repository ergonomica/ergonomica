#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/blocks.py

Code block parsing.
"""

import re

from lib.lang.error import ErgonomicaError

def get_code_blocks(string):
    lines = re.split(r"(?:\"[^\"]*\"|.)+", string)
    blocks = []

    for line in lines:
        if line == "":
            pass
        elif line[0] != " ":
            blocks.append(line)
        else:
            if (not line.startswith("   ")) and (line.startswith(" ")):
                raise ErgonomicaError("[ergo: SyntaxError]: Incorrect indentation on line '%s'." % line)
            else:
                blocks[-1] += line[3:] + "\n"

            
    return blocks

def are_multiple_blocks(string):
    return len(get_code_blocks(string)) > 1 or string[0] == "\n" or ":\n" in string
