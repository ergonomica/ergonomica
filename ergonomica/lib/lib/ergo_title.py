#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/title.py]

Defines the "title" command.
"""

import sys
from ergonomica.lib.lang.error import ErgonomicaError


def ergo_title(argc):
    """title: Set the title of the current terminal window to TITLE.

    Usage:
        title TITLE
    """
    
    sys.stdout.write("\x1b]2;%s\x07" % (argc.args['TITLE']))
    return

