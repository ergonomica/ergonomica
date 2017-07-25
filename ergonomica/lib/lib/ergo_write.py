#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_write.py]

Defines the "write" command.
"""


def write(argc):
    """write: Write STDIN to file FILE.

    Usage:
        write <file>FILE
    """

    open(argc.args['FILE'], 'w').write('\n'.join(argc.stdin))


exports = {'write': write}
