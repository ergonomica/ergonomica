#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/write.py]

Defines the "write" command.
"""


def main(argc):
    """write: Write STDIN to file FILE.

    Usage:
        write FILE
    """

    open(argc.args['FILE'], 'w').write('\n'.join(argc.stdin))
