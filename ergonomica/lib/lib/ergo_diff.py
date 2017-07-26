#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_diff.py]

Differentiate two arrays.
"""

import os
import time

def diff(argc):
    """diff: Differentiate two arrays.
    
    Usage:
        diff [ARRAY1...]
    """
    
    return list(set(argc.stdin) ^ set(argc.args['ARRAY1']))
    

exports = {'diff': diff}