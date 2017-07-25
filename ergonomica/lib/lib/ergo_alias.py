#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_alias.py]

Defines the "alias" command.
"""

def alias(argc):
    """alias: Map commands to names.
    Usage:
        alias NAME FUNCTION
    """

    argc.env.aliases[argc.args['NAME']] = argc.ns[argc.args['FUNCTION']]

exports = {'alias': alias}
