#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/cd.py]

Defines the "cd" command.
"""

import sys
import os
import re


def ergo_cd(args):
    """cd: Changes the directory.
    Usage:
       cd [DIR]
    """
    
    try:
        if args.args['DIR']:
            if args.args['DIR'][0] == "~":
                os.chdir(os.path.expanduser(os.path.expanduser("~")))
            else:
                os.chdir(args.args['DIR'])
        else:
            os.chdir(os.path.expanduser("~"))

        args.env.directory = os.getcwd()
    
    except OSError:
        _, error, _ = sys.exc_info()
        print("[ergo: cd]: " + error)
