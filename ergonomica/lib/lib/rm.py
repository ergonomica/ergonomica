#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/rm.py]

Defines the "rm" command.
"""

import os
import shutil
from ergonomica.lib.lang.error import ErgonomicaError

verbs = {}


def rm(args):
    """<file>...@Remove FILEs (works for directories as well)."""
    print(args.args)
    for x in args.args['<file>']:
        path = os.path.expanduser(x)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        else:
            raise ErgonomicaError("[ergo: NoSuchFileOrDirectoryError]: '%s'." % (path))

verbs["rm"] = rm
