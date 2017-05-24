#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/util/util.py]

Defines various Ergonomica utilities and macros.
"""

import os
import subprocess
import shlex

def run_command(env, cmd):
    """given shell command, returns communication tuple of stdout and stderr"""
    try:
        os.environ["PATH"] = env.PATH
        return subprocess.check_output(shlex.split(cmd), env=os.environ.copy())#, stderr=open(os.devnull, 'wb'))
    except OSError:
        raise Exception


def expand_path(env, path):
    if path[0] == "/":
        pass
    elif path[0] == "~":
        path = os.path.expanduser(path)
    else:
        if path[0:2] == './':
            path = path[2:]
        path = os.path.join(env.directory, path)
    return path
