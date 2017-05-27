#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/environment.py]

Defines the "environment" command.
"""


import os
import sys


def ergo_environment(argc):
    """
       environment: Configure environment variables.

       Usage:
          environment set VARIABLE VALUE
          environment macro add REGEXP REPLACEMENT
          environment alias add COMMAND REPLACEMENT
    """

    if argc.args['set']:
        setattr(argc.env, argc.args['VARIABLE'], argc.args['VALUE'])
        if argc.args['VARIABLE'] == 'path':
            os.environ['PATH'] = argc.args['VALUE']
        elif argc.args['VARIABLE'] == 'pypath':
            sys.path = argc.args['VALUE'].split(os.pathsep)
