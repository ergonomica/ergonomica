#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/mv.py]

Defines the "mv" command.
"""

import shutil
from ergonomica.lib.util.util import expand_path


def mv(argc):
    """mv: Move files.

    Usage:
       mv TARGET DESTINATION
    """

    shutil.move(expand_path(argc.env, argc.args['TARGET']),
                expand_path(argc.env, argc.args['DESTINATION']))
    return


exports = {'mv': mv}

