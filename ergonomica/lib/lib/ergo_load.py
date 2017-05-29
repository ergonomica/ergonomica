#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_load.py]

Defines the "load" command.
"""

import os
import sys

from ergonomica.lib.util.util import expand_path


def main(argc):
    """
    load: Load a file into ergonomica.

    Usage:
       load FILE
    """

    sys.path[0:0] = expand_path(argc.env, ".")
    module = __import__(argc.args['FILE'], locals(), globals())
    argc.ns[argc.args['FILE']] = module.main
    return
