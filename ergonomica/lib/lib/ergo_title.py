#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/title.py]

Defines the "title" command.
"""

import sys


def title(argc):
    """title: Set the title of the current terminal window to TITLE.

    Usage:
        title TITLE
    """

    sys.stdout.write("\x1b]2;%s\x07" % (argc.args['TITLE']))
    return


exports = {'title': title}


