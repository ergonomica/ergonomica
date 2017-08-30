#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/util/util.py]

Defines various Ergonomica utilities and macros.
"""

import os

def expand_path(env, path):
    """Convert a path with an environment to an absolute path."""
    if path[0] == "/":
        pass
    elif path[0] == "~":
        path = os.path.expanduser(path)
    else:
        if path[0:2] == './':
            path = path[2:]
        path = os.path.join(env.directory, path)
    return path


