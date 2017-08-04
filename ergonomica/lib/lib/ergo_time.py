#!/usr/bin/python
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

    return strftime(argc.args['FORMAT'], gmtime())


exports = {'time': time}
