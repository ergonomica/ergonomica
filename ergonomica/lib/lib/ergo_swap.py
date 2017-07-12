#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_swap.py]

Defines the "swap" command.
"""

import os
import shutil
import subprocess
from ergonomica.lib.lang.error import ErgonomicaError


def main(argc):
    """swap: Swap the names/contents of two files.

    Usage:
        swap <file>FILE1 <file>FILE2
    """
    temp_popen = subprocess.Popen(["mktemp", "-d"], stdout=subprocess.PIPE)
    tempfile = temp_popen.communicate()[0].replace("\n", "")

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
    shutil.move(file1, tempfile)

    # move 2 to 1
    shutil.move(file2, file1)

    # move temp to 1
    shutil.move(tempfile + "/" + os.path.basename(file1), file2)

    return
