#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/suplemon.py]

Defines the "suplemon" command (using the suplemon editor).
"""

import os
import sys
sys.path[0] = os.path.join(sys.path[0], "lib")
from lib.suplemon.cli import main

verbs = {}

def suplemon(env, args, kwargs):
    """[FILE,...]@Edit a file."""
    main(args)
    return
        
verbs["suplemon"] = suplemon
