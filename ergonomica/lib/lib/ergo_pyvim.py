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

from pyvim.entry_points.run_pyvim import run

verbs = {}

def pyvim(argc):
    """
    pyvim: Pure Python Vim clone.

    Usage:
       pyvim [FILES...]
    """

    """@EDIT"""
    run(argc.args['FILES'])
    
verbs["pyvim"] = pyvim
