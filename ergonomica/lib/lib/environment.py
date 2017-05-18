#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/environment.py]

Defines the "environment" command.
"""

import os
import sys

verbs = {}

def environment(args):
    """VARIABLE ATTRIBUTE@Set the value of VARIABLE to ATTRIBUTE in the environment."""
    setattr(args.env, args.args['VARIABLE'], args.args['ATTRIBUTE'])
    if args.args['VARIABLE'] == 'path':
        sys.path = args.args['ATTRIBUTE'].split(os.pathsep)
    
verbs["environment"] = environment
