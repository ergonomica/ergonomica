#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/load.py]

Defines the "load" command.
"""

import os
import sys

from ergonomica.lib.util.util import expand_path


def ergo_load(argc):
    """
    load: Load a file into ergonomica.

    Usage:
       load FILE
    """

    sys.path[0:0] = expand_path(argc.env, ".")
    module = __import__(argc.args['FILE'])
    argc.ns.update(module.verbs)
    return
