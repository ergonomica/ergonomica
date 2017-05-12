#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/cd.py]

Defines the "cd" command.
"""

import sys
import os
import re
from ergonomica.lib.lang.error import ErgonomicaError

verbs = {}

def cd(args):
    """[DIR]@Changes to directory DIR. If none specified, changes to ~."""
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
        print("[ergo: cd]: ", error)


verbs["cd"] = cd

