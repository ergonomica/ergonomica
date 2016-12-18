#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# pylint doesn't know where this is being imported
# pylint: disable=import-error

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
    """DIR@Changes to a directory."""
    try:
        if args == []:
            os.chdir(os.path.expanduser("~"))
        elif args[0][0] in ["~", "/"]:
            os.chdir(args[0])
        else:
            os.chdir(env.directory + "/" + args[0])
        env.directory = os.getcwd()
    except OSError:
        _, error, _ = sys.exc_info()
        raise ErgonomicaError("[ergo: NoSuchDirectoryError] No such directory '%s'." % (re.findall(r"'(.*?)'", str(error))[0]))

verbs["cd"] = cd
verbs["chdir"] = cd
verbs["directory"] = cd
