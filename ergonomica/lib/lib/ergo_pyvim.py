#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_pyvim.py]

Defines the "pyvim" command.
"""

from __future__ import unicode_literals

import os
import sys
import subprocess


from ergonomica.lib.lang.error import ErgonomicaError

#sys.path[0] = os.path.join(sys.path[0], "lib", "pyvim")

from pyvim.entry_points.run_pyvim import run

verbs = {}

def pyvim(argc):
    #"""[FILE...]@Edit FILEs in pyvim."""
    """@EDIT"""
    run([])
    
verbs["pyvim"] = pyvim
