#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/argument-verifier.py]

Automatically verify argument lists against docstring specs.
"""

import re

def both_match(exp, a, b):
    return (re.match(exp, a).group(0) == a) and (re.match(exp, b).group(0) == b)

def check_args(string, args):
    # split("@")[0] takes out arg list (not description)) from docstring
    s_args = string.split("@")[0].split()

    # loop variables
    i = 0
    done = False
    
    for s_arg in s_args:

        for i in range(len(args)):
            # 4 types of docstring arguments (BASH/UNIX-style)
            # REQUIRED-ARG      (REQARG  ) (required)
            # OPTIONAL-OPTION   ([-a ARG]) (not required)
            # REQUIRED-OPTION   (-r REQ  ) (required)
            # OPTIONAL-FLAG     ([-a]    ) (not required)

            # REQUIRED_ARG
            if both_match("[a-z]+", arg, s_arg):
                

            elif both_match("-[a-zA-z] .*", arg, s_arg):
            
            elif re.match("-[a-zA-z] .*+", arg).group(0) == arg:

            
            elif re.match("\[-[a-zA-Z] .*\]", arg).group(0) == arg:

            
            elif re.match("\[-[a-zA-Z]\]", arg).group(0) == arg:

        
        
