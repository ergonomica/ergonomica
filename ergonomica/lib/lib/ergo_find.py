#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        find file [-f | --flat]
        find dir [-f | --flat]
        find all [-f | --flat]
        find file PATTERN [-f | --flat] [-s | --strict-path]
        find dir PATTERN [-f | --flat] [-s | --strict-path]
        find all PATTERN [-f | --flat] [-s | --strict-path]
        find string PATTERN [-f | --flat]
        find DIR file PATTERN [-f | --flat] [-s | --strict-path]
        find DIR dir PATTERN [-f | --flat] [-s | --strict-path]
        find DIR all PATTERN [-f | --flat] [-s | --strict-path]
        find DIR string PATTERN [-f | --flat]

    Options:
    -f --flat         Do not search recursively (search only the current directory).
    -s --strict-path  Require that file regexp matches full path to the file.

    """

    global SHARED_ARGC

    SHARED_ARGC = argc

    directory = "." if not argc.args['DIR'] else argc.args['DIR']
    argc.args['PATTERN'] = ".*" if not argc.args['PATTERN'] else argc.args['PATTERN']

    if argc.args['file'] or argc.args['dir'] or argc.args['all']:
        operation = file_match

    elif argc.args['string']:
        operation = string_match

    if argc.args['file'] or argc.args['dir'] or argc.args['all'] or  argc.args['string']:
        if argc.args['--flat']:
            files = os.listdir(directory)
        else:
            # this variable is thrown away, but needed for getting the iteration correct
            # pylint: disable=unused-variable
            files = [os.path.join(root, x) for root, subdirs, files in os.walk(directory) for x in os.listdir(root)]
            if argc.args['dir']:
                files = [_dir for _dir in files if os.path.isdir(_dir)]
            elif argc.args['file'] or argc.args['string']:
                files = [_file for _file in files if os.path.isfile(_file)]

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



