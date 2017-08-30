#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_write.py]

Defines the "write" command.
"""

from ergonomica.lib.util.util import expand_path


def write(argc):
    """write: Write STDIN to file FILE.

    Usage:
        write [-a] <file>FILE [STRING...]
    """

    mode = 'w'
    if argc.args['-a']:
        mode = 'a'
    open(expand_path(argc.env, argc.args['FILE']), mode).write('\n'.join(argc.args['STRING']) + "\n")


exports = {'write': write}


