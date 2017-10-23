#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/lang/environment.py]

The environment manager for Ergonomica. Defines the Environment class which has various session
attributes. Defines ENV as an instance of this Environment.
"""

import os
import getpass
import subprocess
import platform
import multiprocessing
from colorama import Fore

# names match POSIX/vernacular standards
# pylint: disable=invalid-name

try:
    unicode()
except NameError:
    # redefined-builtin for py2/3 support
    unicode = str # pylint: disable=redefined-builtin

class Environment(object):
    """The Ergonomica session environment class."""
    def __init__(self):
        self.run = True
        self.directory = os.getcwd()      # current directory (mutable)
        self.user = getpass.getuser()     # current user
        self.home = os.getenv(key="HOME") # user's home directory
        self.ns = {}                      # function namespace
        self.variables = {}               # variable namespace
        self.macros = {}                  # text macros
        self.welcome = \
r"""
   ____                              _
  / __/______ ____  ___  ___  __ _  (_)______ _
 / _// __/ _ `/ _ \/ _ \/ _ \/  ' \/ / __/ _ `/
/___/_/  \_, /\___/_//_/\___/_/_/_/_/\__/\_,_/
        /___/
"""
        self.theme = {"files": Fore.RED,
                      "match": Fore.GREEN,
                     }

        self.default_color = Fore.WHITE
        self.namespace = {}
        self.editor = "pyvim"
        self.LANG = "EN"
        self.prompt = "[<directory>]\n.: "
        self.editor_mode = False
        self.ergo = lambda x: x
        if "Darwin" in platform.platform() and not (("iPhone" in platform.platform()) or ("iPad" in platform.platform())):
            # i.e., macOS
            self.path = subprocess.check_output(['/usr/libexec/path_helper', '-s'])[6:-16]

        else:
            self.path = os.getenv("PATH")
        self.aliases = {}
        self.modules = {}
        self.cpu_count = multiprocessing.cpu_count()
        self.toolbar = ""
        self.rprompt = ""
        self.pipe_format_string = ''
        self.pipe_progress_char = '='
        self.pipe_progress_length = 15
        


    def change_directory(self, newpath):
        """Change the environment directory."""
        os.chdir(newpath)
        self.directory = newpath

    def get_prompt(self):
        """Return the formatted prompt string."""
        return unicode(self.prompt.replace("<user", self.user)\
                       .replace("<directory>", self.directory))

    def update_env(self):
        """Return a modified os.environ with correct environment variables set."""
        old_env = os.environ.copy()
        os.environ['EDITOR'] = self.editor
        os.environ['PATH'] = self.path


