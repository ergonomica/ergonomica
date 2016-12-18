#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/environment.py]

The environment manager for Ergonomica. Defines the Environment class which has various session
attributes. Defines ENV as an instance of this Environment.
"""

# dumb standard
# pylint: disable=too-few-public-methods

# EDITOR is standard name
# pylint: disable=invalid-name

import os
import getpass

class Environment(object):
    """The Ergonomica session environment class."""
    def __init__(self):
        self.run = True
        self.directory = os.getcwd()
        self.user = getpass.getuser()
        self.home = os.getenv(key="HOME")
        self.verbs = {}
        self.macros = {}
        self.namespace = {}
        self.EDITOR = "emacs"
        self.prompt = "[\\u@\\w]\n$ "
        self.editor_mode = False
