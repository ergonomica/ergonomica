#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/rm.py]

Defines the "rm" command.
"""

import os
import shutil
from ergonomica import ErgonomicaError

def rm(argc):
    """rm: Remove files and directories.

    Usage:
       rm <file/directory>[FILES...]
    """

    for _file in argc.args['FILES']:
        if _file[0] == "/":
            path = _file
        elif _file[0] == "~":
            path = os.path.expanduser(_file)
        else:
            path = os.path.join(argc.env.directory, _file)

        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.islink(path):
                os.unlink(path)
            else:
                os.remove(path)
        else:
            raise ErgonomicaError("[ergo: rm]: NoSuchFileOrDirectoryError: '%s'." % (path))

exports = {'rm': rm}



