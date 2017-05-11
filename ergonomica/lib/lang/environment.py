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
import ConfigParser
import multiprocessing
from colorama import Fore

CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), '.ergo', '.ergo_profile')

class Environment(object):
    """The Ergonomica session environment class."""
    def __init__(self):
        self.run = True                   # 
        self.directory = os.getcwd()      # current directory (mutable)
        self.user = getpass.getuser()     # current user
        self.home = os.getenv(key="HOME") # user's home directory
        self.verbs = {}                   # function namespace
        self.variables = {}               # variable namespace
        self.macros = {}                  # text macros
        self.welcome = """
   ____                              _\n  / __/______ ____  ___  ___  __ _  (_)______ _\n / _// __/ _ `/ _ \\/ _ \\/ _ \\/  ' \\/ / __/ _ `/\n/___/_/  \\_, /\\___/_//_/\___/_/_/_/_/\\__/\\_,_/\n        /___/\n"""

        self.theme = {"files":Fore.RED,
                      "match":Fore.GREEN,
                     }
        self.default_color = Fore.WHITE
        self.namespace = {}
        self.EDITOR = "pyvim"
        self.LANG = "EN"
        self.prompt = "[<user>@<directory>]\n$ "
        self.editor_mode = False
        self.ergo = lambda x: x
        self.PATH = ""
        self.aliases = {}
        self.modules = {}
        self.cpu_count = multiprocessing.cpu_count()
        
    def change_directory(self, newpath):
        """Change the environment directory."""
        os.chdir(newpath)
        self.directory = newpath

# def read_environments(config_path):
#     config = ConfigParser.RawConfigParser()
#     config.read(config_path)

#     # getfloat() raises an exception if the value is not a float
#     # getint() and getboolean() also do this for their respective types
#     a_float = config.getfloat('Section1', 'a_float')
#     an_int = config.getint('Section1', 'an_int')
#     print a_float + an_int

# # Notice that the next output does not interpolate '%(bar)s' or '%(baz)s'.
# # This is because we are using a RawConfigParser().
# if config.getboolean('Section1', 'a_bool'):
#     print config.get('Section1', 'foo')

