#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/parser.py]

Lexer module. Contains tokenize().
"""

# pylint doesn't know that `from lib.verbs...` is run from the above dir
# pylint: disable=import-error

# there isn't another elegant way to do it
# pylint: disable=too-many-branches

import re

def tokenize(string):
    """Tokenize ergonomica commands."""

    # bash escaped
    try:
        bash_escaped = re.search("`(.+?)`", string).groups()

        for item in bash_escaped:
            string = string.replace("`" + item + "`", 'bash "' + item + '"')
    except AttributeError:
        pass

    # python escaped
    try:
        python_escaped = re.search("\\\\(.+?)\\\\", string).groups()

        for item in python_escaped:
            string = string.replace("\\" + item + "\\", 'python "' + item + '"')
    except AttributeError:
        pass

    tokens = [""]
    _special = False
    special = ""
    kwargs = []

    for char in string:
        if _special:
            if _special == "{" and char == "}":
                pattern = re.compile(r'''((?:[^;"']|"[^"]*"|'[^']*')+)''')
                split = pattern.split(special)[1::2]
                for item in split:#special.split(","):
                    kwargs.append(item)
                    _special = False
            elif char in ['"', "'"] and _special == char:
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
