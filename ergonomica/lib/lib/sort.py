#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/sort.py]

Defines the "sort" command.
"""

import re
import os
import shutil
import subprocess

verbs = {}

def raw_temp():
    "Return a temporary file."
    return subprocess.Popen(["mktemp", "-d"], stdout=subprocess.PIPE).communicate()[0].replace("\n", "")

def sort(env, args, kwargs):
    """[DIR=.] {exp:expression}@Sorts each file into a folder with name=the match of *exp* in its name."""

    exp = kwargs["exp"]

    for directory in args:

        # files to sort
        files = os.listdir(directory)
        files_index = enumerate(files)

        # make folders to sort
        folders = [re.search(exp, x).group(0) for x in files]

        # in case a directory name is the same as the name of a file
        tempfiles = [raw_temp() for i in files]

        for i, item in files_index:
            shutil.move(files[i], tempfiles[i] + "/" + files[i])
            try:
                os.mkdir(re.search(exp, files[i]).group(0))
            except OSError:
                pass
            shutil.move(tempfiles[i] + "/" + files[i], folders[i] + "/" + os.path.basename(files[i]))

    return

verbs["sort"] = sort
verbs["organize"] = sort
verbs["organise"] = sort
