#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_while.py]

Defines the Ergonomica while loop construct.
"""

from time import sleep

from ergonomica.lib.lang.arguments import ArgumentsContainer


def main(argc):
    """while: While CONDITION returns true, do BODY.

    Usage:
        while [-s <int>SLEEP] CONDITION BODY

    Options:
        -s  Sleep for SLEEP seconds before iterating again.
    """

    if argc.args['-s']:
        while argc.env.ns[argc.args['CONDITION']]:
            sleep(argc.args['SLEEP'])
            argc.env.ns[argc.args['BODY']]()

    else:
        while argc.ns[argc.args['CONDITION']]:
            argc.ns[argc.args['BODY']](ArgumentsContainer(argc.env, argc.ns, argc.stdin, []))
