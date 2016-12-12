#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/completer.py]

The ergonomica runtime.
"""

# pylint doesn't know where this is being imported
# pylint: disable=import-error

import os
from lib.lib import verbs

def completer(text, state):
    """Return a completion for a command."""
    options = [i for i in os.listdir(".") + verbs.keys() if i.startswith(text)]
    if state > 2:
        return None
    if options != []:# len(options):
        return options[0]
    else:
        return None
