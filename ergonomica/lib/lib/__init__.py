"""
[lib/lib/__init__.py]

This module loads all commands from ergonomica.lib/lib into the 'verbs'
dictionary for running.
"""

import sys
from os import listdir, path

# load all commands from commands folder
commands = [x[:-3] for x in listdir(path.dirname(__file__)) if
            x not in  ["__init__.py", "__pycache__"] and not x.endswith(".pyc")]

# namespace to hold functions
ns = {}

for item in commands:
    module = __import__(item, locals(), globals())
    ns[item[5:]] = module.main

del sys.path[0]
