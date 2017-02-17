"""
[lib/lib/__init__.py]

This module loads all commands from lib/lib into the 'verbs' dictionary for running.
"""

# lowcase is the standard in other files
# pylint: disable=invalid-name

verbs = {}

commands = [
    "addline",
    "alias",
    "bash",
    "cd",
    "clear",
    "cp",
    "echo",
    "edit",
    "equal",
    "ergo_help",
    "export",
    "find",
    "fish",
    "free",
    "get",
    "length",
    "license",
    "list_modules",
    "load_config",
    "ls",
    "macro",
    "mkdir",
    "mkdir",
    "multiply",
    "mv",
    "nequal",
    "ping",
    "pwd",
    "python",
    "quit",
    "read",
    "removeline",
    "rm",
    "set",
    "shuffle",
    "size",
    "sort",
    "string_find",
    "swap",
    "title",
    "users",
    "version",
    "whoami",
    "write",
    "yes",
    "zsh",
]

for item in commands:
    if (item != "__init__.py") and (item[-4:] != ".pyc"):
        verbs.update(__import__('lib.lib.'+item, globals(), locals(), ['object'], 0).verbs)
