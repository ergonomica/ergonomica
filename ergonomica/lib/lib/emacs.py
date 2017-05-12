#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/emacs.py]

Defines the "emacs" command.
"""

import os
import subprocess

verbs = {}

def emacs(ARG):
    """@Runs Emacs."""
    os.environ['PATH'] = ARG.env.path
    subprocess.check_output("emacs", env=os.environ.copy())
    return
    

verbs["emacs"] = emacs


