#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/find.py]

Defines the "find" command.
"""

import os
import glob
from itertools import chain
from multiprocessing import Pool


def main(argc):
    """find: Find files.

    Usage:
        find file PATTERN [-f | --flat]
        find line PATTERN [-f | --flat]

    Options:
    -f --flat  Do not search recursively.
    
    """

    if argc.args['file']:
        list(chain.from_iterable(glob.glob(os.path.join(x[0], argc.args['PATTERN'])) for x in os.walk('.')))

    elif argc.args['line']:
        regex = argc.args['PATTERN']
        files = [x[0] for x in os.walk(".")]

        # create function for distribution of find operation
        def return_matches_for_file(regex, filename):
            for line in open(filename):
                if re.match(regex, line).group() == line:
                    yield line

        # initialize multiprocessing pool
        p = Pool(env.cpu_count)

        # match (using multiprocessing)
        matches = p.map(return_matches_for_file, files)

        # return flattened list
        return [x for x in y for y in matches]

