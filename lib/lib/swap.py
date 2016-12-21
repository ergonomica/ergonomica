#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/swap.py]

Defines the "swap" command.
"""

import os
import shutil
import subprocess

verbs = {}

def swap(env, args, kwargs):
    """FILE1 FILE2@Swaps filenames."""
    tempfile = subprocess.Popen(["mktemp", "-d"], stdout=subprocess.PIPE)
    tempfile = tempfile.communicate()[0].replace("\n", "")

    file1, file2 = os.getcwd() + "/" + args[0], os.getcwd() + "/" +  args[1]
    
    # move 1 to temp
    shutil.move(file1, tempfile)
    
    # move 2 to 1
    shutil.move(file2, file1)

    # move temp to 1
    shutil.move(tempfile + "/" + os.path.basename(file1), file2)

    return 
    
verbs["swap"] = swap
verbs["switch"] = swap
