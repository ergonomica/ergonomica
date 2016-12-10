#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/edit.py]

Defines the "edit" command.
"""

import os

verbs = {}

def edit(env, args, kwargs):
    """[FILE,...]@Edit a file."""
    os.system(env.EDITOR + " " + " ".join(args))

verbs["edit"] = edit
