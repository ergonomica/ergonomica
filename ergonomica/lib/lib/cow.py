#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/cow.py]

Defines the "cow" command.
"""

from ergonomica.lib.lang.error import ErgonomicaError
 
verbs = {}

def cow(env, args, kwargs):
    """STRING@Make a cow say STRING."""
    if len(args) == 1:
        string = args[0]
        s = " " + "_" * (len(string) + 2) + "\n"
        s += "< %s >\n" % string
        s += " " + "-" * (len(string) + 2)
        s += """
        \\   ^__^
         \\  (oo)\\_______
            (__)\\        )\\/\\
                ||----w |
                ||     ||"""
        return s
    else:
        raise ErgonomicaError("[ergo: Wrong number of arguments for 'cow' command.")
    
verbs["cow"] = cow
