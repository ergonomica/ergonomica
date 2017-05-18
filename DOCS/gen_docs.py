#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[DOCS/gen_docs.py]

Automatic docs generation for Ergonomica, in Ergonomica.
"""

import ergonomica
from ergonomica.lib.util import expand_path
from ergonomica.lib.lib import commands

def make_title(string):
    return string + "\n" + " " * len(string)

def gen_docs(argc):
    """TARGETDIR@Build Ergonomica documentation in directory TARGETDIR."""
    target = expand_path(argc.args['TARGETDIR'])
        
    # load into reST format
    for command in commands:
        filedoc = getattr(ergonomica.lib.lib, command).__doc__
        
    
    # dump to file
    
