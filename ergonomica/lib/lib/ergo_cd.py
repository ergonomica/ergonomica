#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_cd.py]

Defines the "cd" command.
"""

import sys
import os
from ergonomica.lib.util.util import expand_path

def main(argc):
    """cd: Changes the directory.

    Usage:
        cd <directory>[DIR]
    """


    if not argc.args['DIR']:
        argc.args['DIR'] = "~"

    os.chdir(expand_path(argc.env, argc.args['DIR']))

    argc.env.directory = os.getcwd()

    return None

