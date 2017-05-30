#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_removeline.py]

Defines the "removeline" command.
"""

import os
from ergonomica.lib.util.util import expand_path


def main(argc):
    """removeline: Remove lines with indices LINENUM from FILE.

    Usage:
        removeline (-f FILE) <int>LINENUM...

    Options:
        -f --file  Specify the file to operate on.
    """

    _file = expand_path(argc.env, argc.args['FILE'])

    # read lines and delete file
    lines = open(_file, "rb").readlines()
    os.remove(_file)

    # delete line
    for item in argc.args['LINENUM']:
        lines[int(item)] = None

    # write to file
    lines = [x for x in lines if x is not None]
    open(argc.args["FILE"], "w").writelines(lines)

    return
