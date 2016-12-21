#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/edit.py]

Defines the "edit" command.
"""
import os
import sys
print sys.path
sys.path[0] = os.path.join(sys.path[0], "lib")
from lib.suplemon.cli import main

verbs = {}

def suplemon(env, args, kwargs):
    """[FILE,...]@Edit a file."""
    main(args)
    return
        
verbs["suplemon"] = suplemon
