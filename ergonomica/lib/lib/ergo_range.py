#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_range.py]

Defines the "range" command.
"""

import sys
import os
from ergonomica import ErgonomicaError
from ergonomica.lib.util.util import expand_path

def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step

def _range(argc):
    """range: Construct a range of integers.

    Usage:
        range END
        range START END
        range START END STEP
    """

    end = float(argc.args['END'])
    try:
        if argc.args['START']:
            start = float(argc.args['START'])
            if argc.args['STEP']:
                step = float(argc.args['STEP'])
                return [x for x in frange(start, end, step)]
            else:
                return [x for x in frange(start, end, 1)]
        else:
            return [x for x in frange(0, end, 1)]

    except ValueError:
        # TODO: have this give the actual offending number
        raise ErgonomicaError("[ergo: range]: Non-number passed.")


exports = {'range': _range}


