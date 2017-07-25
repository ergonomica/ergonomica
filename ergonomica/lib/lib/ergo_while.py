#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_while.py]

Defines the Ergonomica while loop construct.
"""

from time import sleep

from ergonomica.lib.lang.arguments import ArgumentsContainer


def _while(argc):
    """while: While CONDITION returns true, do BODY.

    Usage:
        while CONDITION BODY
    """

    while argc.ns[argc.args['CONDITION']](ArgumentsContainer(argc.env, argc.ns, argc.stdin, [])):
        yield argc.ns[argc.args['BODY']](ArgumentsContainer(argc.env, argc.ns, argc.stdin, []))

exports = {'while': _while}
