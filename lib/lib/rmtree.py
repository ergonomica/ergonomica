#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/rmtree.py]

Defines the "rmtree" command.
"""

import shutil

verbs = {}

def rmtree(env, args, kwargs):
    """FILE,...@Finds a file with a pattern"""
    for _file in args:
        shutil.rmtree(_file)
    return

verbs["rmtree"] = rmtree
