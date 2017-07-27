#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_multiply.py]

Defines the "multiply" command.
"""

from operator import mul
from ergonomica.lib.lang.exceptions import ErgonomicaError

def multiply(argc):
    """multiply: Compare equality of arguments.

    Usage:
        multiply NUMBERS...
    """
    
    parsed_numbers = []
    for i in range(len(argc.args['NUMBERS'])):
        try:
            parsed_numbers.append(float(argc.args['NUMBERS'][i]))
        except ValueError:
            print("[ergo: multiply]: '{}' (index={}) not a number".format(argc.args['NUMBERS'][i], i))
            
    return reduce(mul, parsed_numbers, 1)

exports = {"*": multiply}
