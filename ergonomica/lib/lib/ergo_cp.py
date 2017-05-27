#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_cp.py]

Defines the "cp" command.
"""

import shutil
from ergonomica.lib.util.util import expand_path


def ergo_cp(argc):
    """cp: Copy files.

    Usage:
        cp SOURCE DESTINATION
    """

    shutil.copy2(expand_path(argc.env, argc.args['SOURCE']), expand_path(argc.env, argc.args['DESTINATION']))
    return
