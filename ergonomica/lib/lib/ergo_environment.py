#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/environment.py]

Defines the "environment" command.
"""

import os
import sys


def environment(argc):
    """
       environment: Configure environment variables.

       Usage:
          environment set VARIABLE VALUE
          environment get VARIABLE
    """

    if argc.args['set']:
        vars(argc.env)[argc.args['VARIABLE']] = argc.args['VALUE']
        if argc.args['VARIABLE'] == 'path':
            os.environ['PATH'] = argc.args['VALUE']
        elif argc.args['VARIABLE'] == 'pypath':
            sys.path = argc.args['VALUE'].split(os.pathsep)


    elif argc.args['get']:
        return vars(argc.env)[argc.args['VARIABLE']]

exports = {'environment': environment}


