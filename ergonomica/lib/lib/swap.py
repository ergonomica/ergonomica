#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/swap.py]

Defines the "swap" command.
"""

import os
import shutil
import subprocess
from lib.lang.error import ErgonomicaError

verbs = {}

def swap(env, args, kwargs):
    """FILE1 FILE2@Swaps filenames of FILE1 and FILE2."""
    temp_popen = subprocess.Popen(["mktemp", "-d"], stdout=subprocess.PIPE)
    tempfile = temp_popen.communicate()[0].replace("\n", "")

    # set up proper paths to files
    curdir = os.getcwd()
    file1 = os.path.join(curdir, args[0])
    file2 = os.path.join(curdir, args[1])

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

verbs["swap"] = swap
verbs["switch"] = swap
