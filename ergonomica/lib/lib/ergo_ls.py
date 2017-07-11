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
       ls [DIR...] [-d | --date] [-h | --hide-dotfiles]

    Options:
       -d --date           Show file creation dates.
       -h --hide-dotfiles  Do not show dotfiles.
    """

    # date processing from numerical time
    date = lambda t: str(datetime.datetime.fromtimestamp(creation_date(t))) +\
           " " if argc.args['--date'] else ""
           
    file_filter = lambda x: True

    if argc.args['--hide-dotfiles']:
        file_filter = lambda x: not x.startswith(".")

    if not argc.args['DIR']:
        argc.args['DIR'] = ["."]

    for arg in argc.args["DIR"]:
        return [date(x) + x for x in os.listdir(expand_path(argc.env, arg)) if file_filter(x)]
