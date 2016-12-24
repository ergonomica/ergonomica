#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/rmtree.py]

Defines the "rmtree" command.
"""

import shutil

verbs = {}

def rmtree(env, args, kwargs):
    """FILE,...@Removes the entire directory path to each FILE."""
    for _file in args:
        shutil.rmtree(_file)
    return

verbs["rmtree"] = rmtree
