#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/shuffle.py]

Defines the "shuffle" command.
"""

import random

def ergo_shuffle(env, args):
    """shuffle: Shuffle STDIN.
   
    Usage:
        shuffle
    """
    
    random.shuffle(args)
    return args
