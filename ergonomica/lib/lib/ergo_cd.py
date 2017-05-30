#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_cd.py]

Defines the "cd" command.
"""

import sys
import os
import re


def main(argc):
    """cd: Changes the directory.

    Usage:
        cd [DIR]
    """
    
    try:
        if argc.args['DIR']:
            if argc.args['DIR'][0] == "~":
                os.chdir(os.path.expanduser(os.path.expanduser("~")))
            else:
                os.chdir(argc.args['DIR'])
        else:
            os.chdir(os.path.expanduser("~"))

        argc.env.directory = os.getcwd()
    
    except OSError:
        _, error, _ = sys.exc_info()
        print("[ergo: cd]: ", error)
