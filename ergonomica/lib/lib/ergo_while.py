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
        while [-s SLEEP] CONDITION BODY

    Options:
        -s  Sleep for SLEEP seconds before iterating again.
    """

    if argc.args['-s']:
        while argc.env.ns[argc.args['CONDITION']](ArgumentsContainer(argc.env, argc.ns, argc.stdin, []))[0]:
            sleep(float(argc.args['SLEEP']))
            yield argc.env.ns[argc.args['BODY']](ArgumentsContainer(argc.env, argc.ns, argc.stdin, []))

    else:
        while argc.ns[argc.args['CONDITION']](ArgumentsContainer(argc.env, argc.ns, argc.stdin, [])):
            yield argc.ns[argc.args['BODY']](ArgumentsContainer(argc.env, argc.ns, argc.stdin, []))
