#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/cd.py]

Defines the "cd" command.
"""

import sys
import os
import re
from lib.lang.error import ErgonomicaError

verbs = {}

def cd(env, args, kwargs):
    """[DIR]@Changes to directory DIR. If none specified, changes to ~."""
    try:
        if args == []:
            os.chdir(os.path.expanduser("~"))

        elif args[0][0] in ["~", "/"]:
            os.chdir(os.path.expanduser(args[0]))

        else:
            os.chdir(os.path.join(env.directory, args[0]))

        env.directory = os.getcwd()
    except OSError:
        _, error, _ = sys.exc_info()

        raise ErgonomicaError("[ergo: NoSuchDirectoryError] No such directory '%s'. Perhaps it's a file?" % (re.findall(r"'(.*?)'", str(error))[0]))

verbs["cd"] = cd
verbs["chdir"] = cd
verbs["directory"] = cd
