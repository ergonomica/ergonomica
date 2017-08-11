#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_temp.py]

Defines the "temp" command.
"""

import tempfile

def temp(argc):
    """temp: Generate a temporary file or directory.

    Usage:
        temp (file | dir)
    """

    if argc.args['file']:
        return tempfile.mktemp()
    
    elif argc.args['dir']:
        return tempfile.mkdtemp()


exports = {'temp': temp}
