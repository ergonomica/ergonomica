#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_time.py]

Defines the "time" command.
"""

from time import gmtime, strftime


def time(argc):
    """
    time: Display the current time. FORMAT is in strftime format.

    Usage:
        time [FORMAT]
    """

    format_string = argc.args['FORMAT'] if argc.args['FORMAT'] else "%b %d %Y %H:%M:%S"

    return strftime(format_string, gmtime())


exports = {'time': time}


