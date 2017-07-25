#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_match.py]

Defines the "match" command.
"""

import re # for actual matching


def match(argc):
    """match: Apply regexp to STDIN.

    Usage:
        match REGEXP
    """

    matches = [re.match(argc.args['REGEXP'], x) for x in argc.stdin]

    return [x.group() for x in matches if x]


exports = {'match': match}
