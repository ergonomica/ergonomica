#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_edit.py]

Defines the "edit" command.
"""

from __future__ import unicode_literals

import os
import sys
import subprocess

from ergonomica.lib.lang.error import ErgonomicaError

sys.path[0] = os.path.join(sys.path[0], "lib", "pyvim")

from pyvim.entry_points.run_pyvim import run


def ergo_edit(env, args, kwargs):
    """[FILE,...]@Edit FILEs. Uses EDITOR set in .ergo_profile."""
    try:
        if env.EDITOR == "pyvim":
            run(args)
        subprocess.call([env.EDITOR] + args)
    except OSError:
        try:
            subprocess.call([env.EDITOR])
            raise ErgonomicaError("[ergo: EditorError]: Unable to edit one or more files passed to edit.")
        except OSError:
            raise ErgonomicaError("[ergo: EditorError]: No such editor '%s'." % (env.EDITOR))
    return
