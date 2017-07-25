#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_size.py]

Defines the "size" command.
"""

import os
from ergonomica.lib.lang.error import ErgonomicaError

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
        size [-u UNIT] FILE...

    Options:
        -u, --unit  Specify the unit of size in which to display the file.

    """

    out = []
    size_factor = 1
    if argc.args['--unit']:
        unit = argc.args["UNIT"]
        if unit in SHORT_SIZES:
            size_factor = SHORT_SIZES.index(unit)
        elif unit in SIZES:
            size_factor = SIZES.index(unit)
        elif unit in NAME_SIZES:
            size_factor = NAME_SIZES.index(unit)

    for item in argc.args['FILE']:
        try:
            path = os.path.expanduser(item)
            if not os.path.exists(path):
                raise OSError
            size = file_or_dir_size(path)
            out.append(item + ": " + str(size / 1024 ** size_factor) + " " + SIZES[size_factor])
        except OSError:
            raise ErgonomicaError("[ergo: NoSuchFileError]: No such file '%s'." % (item))

    return out


exports = {'size': size}
