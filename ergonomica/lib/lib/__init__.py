"""
[lib/lib/__init__.py]

This module loads all commands from ergonomica.lib/lib into the 'verbs' dictionary for running.
"""

import os

verbs = {}

files = os.listdir(os.path.dirname(__file__))

commands = []

for command in files:
    parsed_command = command.split(".")[0]
    if parsed_command == "__init__":
        pass
    elif parsed_command not in files:
        commands.append(parsed_command)

for item in commands:
    if (item != "__init__.py") and (item[-4:] != ".pyc"):
        verbs.update(__import__('ergonomica.lib.lib.'+item, globals(), locals(), ['object'], 0).verbs)
