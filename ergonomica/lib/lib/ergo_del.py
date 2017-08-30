#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_del.py]

Defines the "del" command.
"""

from ergonomica import ErgonomicaError

def _del(argc):
    """del: Delete variables.

    Usage:
       del [<variable>VARS...]
    """

    for var in argc.args['VARS']:
        try:
            del argc.ns[var]
        except KeyError:
            raise ErgonomicaError("[ergo: del]: No such variable '{}'.".format(var))

exports = {'del': _del}


