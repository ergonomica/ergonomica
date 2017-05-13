#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/emacs.py]

Defines the "emacs" command.
"""

import os
import subprocess

verbs = {}

def emacs(argc):
    """[FILE...]@Runs Emacs."""
    os.environ['PATH'] = argc.env.path
    command = ["emacs"]
    if argc.args['FILE']:
        command.append(argc.args['FILE'])
    subprocess.check_output(command, env=os.environ.copy())
    return
    

verbs["emacs"] = emacs


