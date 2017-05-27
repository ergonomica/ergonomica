"""
[lib/lib/__init__.py]

This module loads all commands from ergonomica.lib/lib into the 'verbs'
dictionary for running.
"""

import sys
from os import listdir, path

# load all commands from commands folder
commands = [x[:-3] for x in listdir(path.dirname(__file__)) if
            x != "__init__.py" and not x.endswith(".pyc")]

# namespace to hold functions
ns = {}

for item in commands:
    module = __import__(item, locals(), globals())

    ns[item[5:]] = getattr(module, item)

print(ns)

del sys.path[0]
