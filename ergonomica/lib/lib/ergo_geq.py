#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/geq.py]

Defines the "geq" command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError

def geq(argc):
    """geq: Compare equality of arguments.

    Usage:
        geq ARG1 ARG2
    """
    
    try:
        i = int(argc.args['ARG1'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: {}' not a number.".format(argc.args['ARG1']))
    try:
        j = int(argc.args['ARG2'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: '{}' not a number.".format(argc.args['ARG2']))
        
    return i >= j

exports = {">=": geq}
