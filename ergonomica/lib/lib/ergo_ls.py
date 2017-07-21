#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ls.py]

Defines the "ls" command.
"""

import os
import datetime
from ergonomica.lib.util.util import expand_path
from ergonomica.lib.lang.stat import creation_date


def main(argc):
    """
    ls: List files in a directory.

    Usage:
        ls <directory>[DIR] [-c | --count-files][-d | --date] [-h | --hide-dotfiles]

    Options:
        -d --date           Show file creation dates.
        -h --hide-dotfiles  Ignore dotfiles.
        -c --count-files    Return the number of files in a directory.
    
    Examples:
        ls $ 
    """


    file_filter = lambda x: True

    if argc.args['--hide-dotfiles']:
        file_filter = lambda x: not x.startswith(".")

    # date processing from numerical time
    date = lambda t: str(datetime.datetime.fromtimestamp(creation_date(t))) +\
           " " if argc.args['--date'] else ""

    if not argc.args['DIR']:
        argc.args['DIR'] = "."


    files = [date(x) + x for x in os.listdir(expand_path(argc.env, argc.args['DIR']))
             if file_filter(x)]
    

    if argc.args['--count-files']:
        return len(files)
    else:
        return files
