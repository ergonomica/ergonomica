#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/sfind.py]

Defines the "sfind" command.
"""

import os
import glob
from itertools import chain

verbs = {}

def find(argc):
    """sfind: Find a string in files.

    Usage:
       find PATTERN [-f | --flat]

    Options:
    -f --flat  Do not search recursively.
    
    """

    #for x in os.walk('.'):
    return list(chain.from_iterable(glob.glob(os.path.join(x[0], argc.args['PATTERN'])) for x in os.walk('.')))
    
verbs['find'] = find
