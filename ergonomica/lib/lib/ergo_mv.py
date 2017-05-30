#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/mv.py]

Defines the "mv" command.
"""

import shutil
from ergonomica.lib.util.util import expand_path


def main(argc):
    """mv: Move files.

    Usage:
       mv TARGET DESTINATION
    """

    shutil.move(expand_path(argc.env, argc.args['TARGET']), argc.args['DESTINATION'])
    return
