#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/addline.py]

Defines the "addline" command.
"""

import os
#from ergonomica.lib.lang.error import ErgonomicaError

verbs = {}

def addline(env, args):
    """[LINE,...] -file FILENAME@Adds all LINEs to file filename. Note that newlines must be included."""
    #if not ("-file" in args):
    #    print("[ergo: addline]: No file specified for addline.")

    lines = []
    _file = ""

    skip = False

    for i in range(len(args)):
        if skip:
            skip = False
            continue
        elif args[i] == '-file':
            _file = args[i + 1]
            skip = True
            continue
        else:
            lines.append(args[i])
    
    if _file[0] not in ["/", "~"]:
        _file = os.path.join(env.directory, _file)
    for line in args:
        open(_file, "a").write(line + "\n")
    return


verbs["addline"] = addline
verbs["append"] = addline
