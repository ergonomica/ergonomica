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

    if re.match(SHARED_ARGC.args['PATTERN'], _file).group() == _file:
        return [_file]

    return ""


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

    global SHARED_ARGC

    SHARED_ARGC = argc

    if argc.args['file']:
        operation = file_match

    elif argc.args['string']:
        operation = string_match


    if argc.args['file'] or argc.args['string']:
        # this variable is thrown away, but needed for getting the iteration correct
        # pylint: disable=unused-variable
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames]


        # initialize multiprocessing pool
        pool = Pool(argc.env.cpu_count)

        # match (using multiprocessing)
        matches = pool.map(operation, files)

        # return output with False filtered out
        flattened_matches = []
        for i in matches:
            flattened_matches += i

        return flattened_matches

    return [x for x in argc.stdin if re.match(argc.args['PATTERN'], x)
            and re.match(argc.args['PATTERN'], x).group() == x]
