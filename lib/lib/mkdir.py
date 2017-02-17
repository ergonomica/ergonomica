#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/mkdir.py]

Defines the "mkdir" command.
"""

import os
import errno
import shutil
from lib.lang.error import ErgonomicaError

verbs = {}


def mkdir(env, args, kwargs):
    """[DIR,...]@Make DIRs."""
    for directory in args:
        try:
            os.mkdir(os.path.expanduser(directory))
        except OSError:
            if errno.EEXIST:
                if kwargs.get("overwrite") == 'true':
                    shutil.rmtree(os.path.expanduser(directory))
                    os.mkdir(os.path.expanduser(directory))
                else:
                    raise ErgonomicaError('[ergo: DirectoryExist]')  # TODO issue #42


verbs["mkdir"] = mkdir
