#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_slice.py]

Defines the "slice" command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError


def _slice(argc):
    """slice: Slice values of STDIN.

    Usage:
        slice [-s START] [-e END]
    """
    
    if argc.args['START']:
        if argc.args['END']:
            return [x[int(argc.args['START']):int(argc.args['END'])] for x in argc.stdin]
        else:
            return [x[int(argc.args['START']):] for x in argc.stdin]
    else:
        if argc.args['END']:
            return [x[:int(argc.args['END'])] for x in argc.stdin]
        else:
            raise ErgonomicaError("[ergo: slice]: Please specify at least one index to slice by.")


exports = {'slice': _slice}
