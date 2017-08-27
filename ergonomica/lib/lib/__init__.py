#!/usr/bin/python
# -*- coding: utf-8 -*-

# these are the variable standards in other files (called inside functions)
# pylint: disable=invalid-name

"""
[lib/lib/__init__.py]

This module loads all commands from ergonomica.lib/lib into the 'verbs'
dictionary for running.
"""

import sys
from os import listdir, path
from ergonomica.lib.util.setup import setup

PACKAGES_PATH = path.join(path.expanduser("~"), ".ergo")

sys.path[0:0] = [PACKAGES_PATH]
sys.path[0:0] = [path.dirname(__file__)]

def file_exec_shim(filename):
    def f(*argc):
        from ergonomica.lib.lang.interpreter import execfile
        return execfile(filename, *argc)
    return f

# load all commands from commands folder
try:
    commands = [x[:-3] for x in listdir(path.dirname(__file__)) +
                listdir(PACKAGES_PATH) if
                x.endswith(".py") and x != "__init__.py"]
    ergo_commands = [x for x in listdir(PACKAGES_PATH) if x.endswith(".ergo")]

except OSError:
    setup()
    print("Please restart ergonomica.")
    raise SystemExit

# namespace to hold functions
ns = {}

for item in commands:
    try:
        module = __import__(item, locals(), globals())
    except Exception as e:
        print(e)
    ns.update(module.exports)

for item in ergo_commands:
    ns.update({item[:-5]: file_exec_shim(PACKAGES_PATH + "/" + item)})

del sys.path[0]
