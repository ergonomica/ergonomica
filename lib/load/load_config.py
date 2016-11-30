#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/load/load_config.py]

This module loads the config file into the main environment (ENV).
"""

def load_config(environment, lines):
    """Load a config file into environment."""
    for line in [x.split(" ", 1) for x in lines]:
        if line[0] == "EDITOR":
            environment.EDITOR = line[1]
        elif line[0] == "PROMPT":
            environment.prompt = line[1]
