#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/completer.py]

The ergonomica completion engine.
"""

# pylint doesn't know where this is being imported
# pylint: disable=import-error

import os
from lib.lib import verbs

def completer(text, state):
    """Return a completion for a command or directory."""
    options = [i for i in os.listdir(".") + verbs.keys() if i.startswith(text) and len(i) > len(text)]
    if options == []:
        if text.endswith("/"):
            options = [i for i in os.listdir(text) if i.startswith(text) and len(i) > len(text)]
        return None
    if state > 2:
        return None
    if options != []:
        complete_string = ""
        i = 0
        try:
            while True:
                if [x[i] for x in options] == [options[0][i]] * len(options):
                    complete_string += options[0][i]
                i += 1
        except IndexError:
            pass
        return complete_string
