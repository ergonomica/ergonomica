#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/cp.py]

Defines the "cp" command.
"""

import shutil
from ergonomica.lib.util.util import expand_path

verbs = {}

def cp(argc):
    """cp: Copy files.

    Usage:
       cp SOURCE DESTINATION
    """

    #shutil.copy2(argc.args['SOURCE'
    
    return
    
    
    #     for i in range(0, len(args) - 1):
    #         try:
    #             shutil.copy2(env.directory + "/" + args[i], env.directory + "/" + args[i+1])
    #         except OSError:
    #             pass
    # else:
    #     for i in args:
    #         shutil.move(env.directory + "/" + args[i], kwargs["dest"])                
    # return

verbs["cp"] = cp
