#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/cp.py]

Defines the "cp" command.
"""

import shutil
from ergonomica.lib.util.util import expand_path
import errno

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def cp(argc):
    """cp: Copy files.

    Usage:
        cp SOURCE DESTINATION
    """

    copyanything(expand_path(argc.env, argc.args['SOURCE']),
                 expand_path(argc.env, argc.args['DESTINATION']))
    return


exports = {'cp': cp}


