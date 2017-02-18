#!/usr/bin/python
# -*- coding: utf-8 -*-

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

"""
[lib/load/load_config.py]

This module loads the config file into the main environment (ENV).
"""

from __future__ import print_function

import os
from colorama import Fore

def load_config(environment, lines):
    """Load a config file into environment."""
    for line in [x.split(" ", 1) for x in lines]:
        try:
            if line[0].startswith("#"):
                return
            elif not line[0].strip():
                return
            elif line[0] == "EDITOR":
                environment.EDITOR = line[1]
            elif line[0] == "PROMPT":
                environment.prompt = line[1]
            elif line[0] == "ALIAS":
                try:
                    environment.aliases[line[1].split(" IS ")[0]] = line[1].split(" IS ", 1)[1]
                except KeyError:
                    print("[ergo: AliasError]: No such command '%s'." % line[1].split()[1])
            elif line[0] == "PATH":
                environment.PATH += os.pathsep + line[1].replace(" ", os.pathsep)
            elif line[0] == "VAR":
                environment.namespace[line[1].split(" IS ")[0]] = line[1].split(" IS ")[1]
            elif line[0] == "MACRO":
                environment.macros[line[1].split(" IS ")[0]] = line[1].split(" IS ")[1]
            elif line[0] == "THEME":
                environment.theme[line[1].split(" IS ")[0]] = Fore.__dict__[line[1].split(" IS ")[1]]

            elif line[0] == "LANGUAGE":
                if not (line[1] in ["EN", "ES"]):
                    raise Exception()
                else:
                    environment.LANG = line[1]
            
            #elif line[0][0] == "#":
            #    pass
            else:
                print("[ergo: ConfigError]: Error in .ergo_profile, line='%s'. Line not loaded." % (" ".join(line)))
        except:
            print("[ergo: ConfigError]: Error in .ergo_profile, line='%s'. Line not loaded." % (" ".join(line)))
