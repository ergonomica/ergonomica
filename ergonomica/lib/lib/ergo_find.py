#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/find.py]

Defines the "find" command.
"""

import os
import glob
import re
from itertools import chain
from multiprocessing import Pool

shared_argc = []

def file_match(x):
    global shared_argc
    
    if re.match(shared_argc.args['PATTERN'], x).group() == x:
        return [x]
    else:
        return ""

def string_match(x):
    global shared_argc
    
    try:
        matches = []
        for line in open(x).readlines():
            if re.search(shared_argc.args['PATTERN'], line):
                matches.append(x + ': ' + line[:-1].strip())
        return matches
    except IOError:
        return [""]




def main(argc):
    """find: Find patterns.

    Usage:
        find PATTERN
        find file PATTERN [-f | --flat]
        find string PATTERN [-f | --flat]

    Options:
    -f --flat  Do not search recursively.
    
    """

    global shared_argc

    shared_argc = argc
    
    if argc.args['file']:
        op = file_match

    elif argc.args['string']:
        op = string_match

        
    if argc.args['file'] or argc.args['string']:
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames]
    
                
        # initialize multiprocessing pool
        pool = Pool(argc.env.cpu_count)
    
        # match (using multiprocessing)
        matches = pool.map(op, files)
        
        # return output with False filtered out
        flattened_matches = []
        for i in matches:
            flattened_matches += i
            
        return flattened_matches
    
    else:
        return [x for x in argc.stdin if re.match(argc.args['PATTERN'], x) and re.match(argc.args['PATTERN'], x).group() == x]
