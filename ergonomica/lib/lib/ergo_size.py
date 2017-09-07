#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_size.py]

Defines the "size" command.
"""

import os
from ergonomica import ErgonomicaError

SIZES = ["byte(s)", "kilobyte(s)", "megabyte(s)", "gigabyte(s)", "terabyte(s)", "petabyte(s)"]
NAME_SIZES = ["byte", "kilobyte", "megabyte", "gigabyte", "terabyte", "petabyte"]
SHORT_SIZES = ["B", "kB", "MB", "GB", "TB", "PB"]


def file_or_dir_size(path):
    """Return the size of a file or directory."""
    if (os.path.isdir(path)):
        for root, dirs, files in os.walk(path):
            names = files + dirs
            return sum(file_or_dir_size(os.path.join(root, name)) for name in names)
    elif os.path.isfile(path):
        return os.path.getsize(path)
    # Dangling symlinks gets here
    return 0


def size(argc):
    """size: Return the sizes of files.

    Usage:
        size [-h] FILE
        size [-h] [-u UNIT] FILE

    Options:
        -u, --unit            Specify the unit of size in which to display the file.
        -h, --human-readable  Print the size along with units (i.e., human readable)

    """

    path = os.path.expanduser(argc.args['FILE'])
    if not os.path.exists(path):
        raise ErgonomicaError("[ergo: NoSuchFileError]: No such file '%s'." % (argc.args['FILE']))
    size = file_or_dir_size(path)

    if argc.args['--unit']:
        unit = argc.args["UNIT"]
        if unit in SHORT_SIZES:
            size_factor = SHORT_SIZES.index(unit)
        elif unit in SIZES:
            size_factor = SIZES.index(unit)
        elif unit in NAME_SIZES:
            size_factor = NAME_SIZES.index(unit)

    else:
        # automatically calculate the best unit, falling
        # back to largest size if too large
        size_factor = len(SHORT_SIZES) - 1
        for i in range(len(SIZES)):
            if (1024 ** i) >= size:
                size_factor = i - 1
                break


    if argc.args['--human-readable']:
        return argc.args['FILE'] + ": " + str(size / 1024.0 ** size_factor) + " " + SIZES[size_factor]
    else:
        return (size / 1024.0 ** size_factor)




exports = {'size': size}

