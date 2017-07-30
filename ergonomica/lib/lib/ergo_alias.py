#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_alias.py]

Defines the "alias" command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError

def alias(argc):
    """alias: Map another name to an object in the Ergonomica namespace.
    Usage:
        alias NAME FUNCTION
    """

    try:
        argc.ns[argc.args["NAME"]] = argc.ns[argc.args["FUNCTION"]]
    except KeyError:
        if argc.args["NAME"] not in argc.ns:
            raise ErgonomicaError("[ergo: alias]: No such item {}' in namespace.".format(argc.args["NAME"]))
        elif argc.args["FUNCTION"] not in argc.ns:
            raise ErgonomicaError("[ergo: alias]: No such item {}' in namespace.".format(argc.args["FUNCTION"]))


exports = {'alias': alias}
