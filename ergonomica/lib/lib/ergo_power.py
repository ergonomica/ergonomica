#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_power.py]

Defines the "power" command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError

def power(argc):
    """power: Compare equality of arguments.

    Usage:
        power ARG1 ARG2
    """
    
    try:
        i = float(argc.args['ARG1'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: {}' not a number.".format(argc.args['ARG1']))
    try:
        j = float(argc.args['ARG2'])
    except ValueError:
        raise ErgonomicaError("[ergo: geq]: '{}' not a number.".format(argc.args['ARG2']))
        
    return i ** j

exports = {"^": power}
