#!/usr/bin/python
# -*- coding: utf-8 -*-

# needed for sharing variable accross multiple processes
# pylint: disable=global-statement

"""
[lib/lib/find.py]

Defines the "find" command.
"""

import os
import re
from multiprocessing import Pool

SHARED_ARGC = []

def file_match(_file):
    """Returns file if it matches a pattern, else returns ''."""
    global SHARED_ARGC

    if not SHARED_ARGC.args['--strict-path']:
        filename = os.path.basename(_file)
    else:
        filename = _file

    match = re.match(SHARED_ARGC.args['PATTERN'], filename)
    if match and (match.group() == filename):
        return [_file]

    return [False]


def string_match(_file):
    """Returns the line(s) in a file that match a pattern."""
    global SHARED_ARGC

    try:
        matches = []
        for line in open(_file).readlines():
            if re.search(SHARED_ARGC.args['PATTERN'], line):
                matches.append(_file + ': ' + line[:-1].strip())
        return matches
    except IOError:
        return [False]
    except UnicodeDecodeError:
        return [False]


def find(argc):
    """find: Find patterns.

    Usage:
        find PATTERN
        find file PATTERN [-f | --flat] [-s | --strict-path]
        find string PATTERN [-f | --flat]

    Options:
    -f --flat         Do not search recursively (search only the current directory).
    -s --strict-path  Require that file regexp matches full path to the file.

    """

    global SHARED_ARGC

    SHARED_ARGC = argc
    
    if argc.args['file']:
        operation = file_match

    elif argc.args['string']:
        operation = string_match

    elif argc.args['PATTERN']:
        return [x for x in argc.stdin if re.match(argc.args['PATTERN'], x) and re.match(argc.args['PATTERN'], x).group() == x]


    if argc.args['file'] or argc.args['string']:
        if argc.args['--flat']:
            files = os.listdir(".")
        else:
            # this variable is thrown away, but needed for getting the iteration correct
            # pylint: disable=unused-variable
            files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames]


        # initialize multiprocessing pool
        pool = Pool(argc.env.cpu_count)

        # match (using multiprocessing)
        matches = map(operation, files)#pool.map(operation, files)
        

        # return output with False filtered out
        flattened_matches = []
        for i in matches:
            flattened_matches += i

        return [x for x in flattened_matches if x]
        
exports = {'find': find}

