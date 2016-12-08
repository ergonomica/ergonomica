#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/parser.py]

Lexer module. Contains tokenize().
"""

# pylint doesn't know that `from lib.verbs...` is run from the above dir
# pylint: disable=import-error

import re
import subprocess
from lib.verbs import verbs

def tokenize(string):
    """Tokenize ergonomica commands."""
    
    # bash escaped
    try:
        bash_escaped = re.search("`(.+?)`", string).groups()

        for item in bash_escaped:
            cmd = item.split(",")
            evaluated_cmd = subprocess.check_output(cmd, cwd=verbs.directory)
            string = string.replace("`" + item + "`", evaluated_cmd)
    except AttributeError:
        pass

    # python escaped
    try:
        python_escaped = re.search("\\\\(.+?)\\\\", string).groups()

        for item in python_escaped:
            evaluated_item = eval(item, globals())
            string = string.replace("\\" + item + "\\", str(evaluated_item))
    except AttributeError:
        pass

    tokens = [""]
    _special = False
    special = ""
    kwargs = []

    for char in string:
        if _special:
            if char in ["'", '"', "}"]:
                if _special == "{":
                    for item in special.split(","):
                        kwargs.append(item)
                elif _special in ['"', "'"]:
                    tokens.append(special)
                _special = False
            else:
                special += char
        else:
            if char == " ":
                tokens.append("")
            elif char in ["{", '"', "'"]:
                _special = char
                special = ""
            else:
                tokens[-1] += char

           # filter out empty strings
    return [[x for x in tokens if x], kwargs]
