#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_swap.py]

Defines the "swap" command.
"""

import os
import shutil
import tempfile
from ergonomica.lib.lang.exceptions import ErgonomicaError


def swap(argc):
    """swap: Swap the names/contents of two files.

    Usage:
        swap <file>FILE1 <file>FILE2
    """
    tempdir = tempfile.mkdtemp()

    # set up proper paths to files
    curdir = os.getcwd()
    file1 = os.path.join(curdir, argc.args['FILE1'])
    file2 = os.path.join(curdir, argc.args['FILE2'])

    # check existence of files
    if not (os.path.exists(file1)):
        raise ErgonomicaError("[ergo: FileError]: No such file '%s'." % file1)
    elif not (os.path.exists(file2)):
        raise ErgonomicaError("[ergo: FileError]: No such file '%s'." % file2)

    # move 1 to temp
    shutil.move(file1, tempdir)

    # move 2 to 1
    shutil.move(file2, file1)

    # move temp to 1
    shutil.move(tempdir + "/" + os.path.basename(file1), file2)

    return


exports = {'swap': swap}
