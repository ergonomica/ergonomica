#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/load/load_config.py]

This module loads the config file into the main environment (ENV).
"""

from __future__ import print_function

from lib.colorama import Fore

def load_config(environment, lines):
    """Load a config file into environment."""
    for line in [x.split(" ", 1) for x in lines]:
        try:
            if line[0][0] == "\#":
                return
            elif line[0] == "EDITOR":
                environment.EDITOR = line[1]
            elif line[0] == "PROMPT":
                environment.prompt = line[1]
            elif line[0] == "EDITORMODE":
                environment.editor_mode = line[1]
            elif line[0] == "ALIAS":
                try:
                    environment.verbs[line[1].split()[0]] = environment.verbs[line[1].split()[1]]
                except KeyError:
                    print("[ergo: AliasError]: No such command '%s'." % line[1].split()[1])
            elif line[0] == "VAR":
                environment.namespace[line[1].split()[0]] = line[1].split()[1]
            elif line[0] == "MACRO":
                environment.macros[line[1].split()[0]] = line[1].split()[1]
            elif line[0] == "THEME":
                environment.theme[line[1].split()[0]] = Fore.__dict__[line[1].split()[1]]
        except Exception:
            print("[ergo: ConfigError]: Error in .ergo_profile, line='%s'. Line not loaded." % (" ".join(line)))
