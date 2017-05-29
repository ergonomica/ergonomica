#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/mkdir.py]

Defines the "mkdir" command.
"""

import os
import errno
import shutil
from ergonomica.lib.lang.error import ErgonomicaError


def ergo_mkdir(argc):
    """mkdir: Make a directory.
    
    Usage:
       mkdir DIR
    """
    
    try:
        os.mkdir(os.path.expanduser(argc.args['DIR']))
    except OSError:
        if errno.EEXIST:
            if kwargs.get("overwrite") == 'true':
                shutil.rmtree(os.path.expanduser(directory))
                os.mkdir(os.path.expanduser(directory))
            else:
                raise ErgonomicaError('[ergo: DirectoryExist]')  # TODO issue #42
