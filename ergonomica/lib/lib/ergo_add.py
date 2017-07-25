#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_add.py]

Defines the "add" command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError

def add(argc):
    """add: Compare equality of arguments.

    Usage:
        add ARG1 ARG2
    """
    
    try:
        i = int(argc.args['ARG1'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: {}' not a number.".format(argc.args['ARG1']))
    try:
        j = int(argc.args['ARG2'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: '{}' not a number.".format(argc.args['ARG2']))
        
    return i + j

exports = {"+": add}
