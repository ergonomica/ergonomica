#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_sort.py]

Defines the "sort" command.
"""

import re
import os
import shutil
import subprocess


def raw_temp():
    """Return a temporary file."""
    return subprocess.Popen(["mktemp", "-d"],
                            stdout=subprocess.PIPE).communicate()[0].replace("\n", "")

def main(argc):
    """sort: Sort files into folders based on match of regex EXPRESSION in their names.

    Usage:
        sort [DIR=.] EXPRESSION
    """

    exp = argc.args['EXPRESSION']

    for directory in os.listdir(argc.args['DIR']):

        # files to sort
        files = os.listdir(directory)
        files_index = enumerate(files)

        # make folders to sort
        folders = [re.search(exp, x).group(0) for x in files]

        # in case a directory name is the same as the name of a file
        tempfiles = [raw_temp() for i in files]

        # for i, item syntax is not necessarily unclear and saves lines
        # pylint: disable=unused-variable
        for i, item in files_index:
            shutil.move(files[i], tempfiles[i] + "/" + files[i])
            try:
                os.mkdir(re.search(exp, files[i]).group(0))
            except OSError:
                pass
            shutil.move(tempfiles[i] + "/" + files[i],
                        folders[i] + "/" + os.path.basename(files[i]))

    return
