#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/size.py]

Defines the "size" command.
"""

import os
import math
from lib.lang.error import ErgonomicaError

verbs = {}

SIZES = ["byte(s)", "kilobyte(s)", "megabyte(s)", "gigabyte(s)", "terabyte(s)", "petabyte(s)"]

def size(env, args, kwargs):
    """[STRING,...]@Prints its input."""
    out = []
    for item in args:
        try:
            size = 0
            if item[0] in ["/", "~"]:
                size = os.path.getsize(item)
            else:
                size = os.path.getsize(env.directory + "/" + item)
                size_factor = int(math.floor(math.log(size) / 6.93147))
                out.append(item + " : " + str(size / 1024**size_factor) + " " + SIZES[size_factor])
        except OSError:
            raise ErgonomicaError("[ergo: NoSuchFileError]: No such file '%s'." % (item))
    return out

verbs["size"] = size
