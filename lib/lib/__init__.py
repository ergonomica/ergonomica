import os

verbs = {}

commands = ["bash", "cd", "clear", "cp", "echo", "edit", "ergo_help", "find",
            "fish", "get", "ls", "mkdir", "mv", "pwd", "python", "quit", "read",
            "rm", "set", "version", "whoami", "yes", "zsh", "find_string", "multiply",
            "length", "size",
           ]

for item in commands:
    if (item != "__init__.py") and (item[-4:] != ".pyc"):
        verbs.update(__import__('lib.lib.'+item, globals(), locals(), ['object'], -1).verbs)
