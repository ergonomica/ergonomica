#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_leq.py]

Defines the "leq" command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError

def leq(argc):
    """leq: Compare equality of arguments.

    Usage:
        leq ARG1 ARG2
    """
    
    try:
        i = int(argc.args['ARG1'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: {}' not a number.".format(argc.args['ARG1']))
    try:
        j = int(argc.args['ARG2'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: '{}' not a number.".format(argc.args['ARG2']))
        
    return i <= j

exports = {"<=": leq}
