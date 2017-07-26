#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_round.py]

Defines the "round" command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError

def _round(argc):
    """round: Round floating-point numbers.

    Usage:
        round [PRECISION]
    """
    
    if not argc.args['PRECISION']:
        try:
            return [int(float(x)) for x in argc.stdin]
        except ValueError:
            raise ErgonomicaError("[ergo: round]: STDIN not all numbers.")
    
    else:
        try:
            precision = int(argc.args['PRECISION'])
        except ValueError:
            raise ErgonomicaError("[ergo: ^]: '{}' not a number.".format(argc.args['PRECISION']))
        
        try:
            return [round(float(x), precision) for x in argc.stdin]
        except ValueError:
            raise ErgonomicaError("[ergo: round]: STDIN not all numbers.")
    
exports = {"round": _round}
