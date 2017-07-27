#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_del.py]

Defines the "del" command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError

def _del(argc):
    """del: Delete variables.

    Usage:
       del <variable>VAR
    """

    try:
        del argc.ns[argc.args['VAR']]
    except KeyError:
        raise ErgonomicaError("[ergo: del]: No such variable '{}'.".format(argc.args['VAR']))

exports = {'del': _del}
