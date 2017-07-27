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
        add NUMBERS...
    """
    
    parsed_numbers = []
    for i in range(len(argc.args['NUMBERS'])):
        try:
            parsed_numbers.append(float(argc.args['NUMBERS'][i]))
        except ValueError:
            print("[ergo: add]: '{}' (index={}) not a number".format(argc.args['NUMBERS'][i], i))
            
    return sum(parsed_numbers)

exports = {"+": add}
