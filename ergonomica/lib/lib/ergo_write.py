#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_write.py]

Defines the "write" command.
"""

from ergonomica.lib.util.util import expand_path


def write(argc):
    """write: Write STDIN to file FILE.

    Usage:
        write <file>FILE [STRING...]
    """
    
    open(expand_path(argc.env, argc.args['FILE']), 'a').write('\n' + '\n'.join(argc.args['STRING']))


exports = {'write': write}
