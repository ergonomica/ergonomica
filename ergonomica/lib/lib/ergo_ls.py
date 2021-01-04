#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[lib/lib/ls.py]

Defines the "ls" command.
"""

import os
import datetime
from ergonomica.lib.util.util import expand_path
from ergonomica.lib.lang.stat import creation_date
from ergonomica import ErgonomicaError

def ls(argc):
    """
    ls: List files in a directory.

    Usage:
        ls [DIR] [-c | --count-files] [-d | --date] [-a | --all]

    Options:
        -d --date           Show file creation dates.
        -a --all            Do not ignore files and directories starting with a `.` character..
        -c --count-files    Return the number of files in a directory.

    Examples:
        ls $
    """

    # date processing from numerical time
    date = lambda t: str(datetime.datetime.fromtimestamp(creation_date(t))) +\
           " " if argc.args['--date'] else ""

    if not argc.args['DIR']:
        argc.args['DIR'] = "."

        
    if not os.path.isdir(expand_path(argc.env, argc.args['DIR'])):
        raise ErgonomicaError("[ergo: ls]: [DirectoryError]: No such directory '{}'.".format(expand_path(argc.env, argc.args['DIR'])))
    
    files = [date(x) + x for x in os.listdir(expand_path(argc.env, argc.args['DIR']))
             if argc.args['--all'] or (not x.startswith("."))]
    
    if argc.args['--count-files']:
        return len(files)
    else:
        return files

exports = {'ls': ls}


