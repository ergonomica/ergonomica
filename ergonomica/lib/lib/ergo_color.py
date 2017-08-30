#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_color.py]

Defines the "color" command.
"""

import colorama
import re
from ergonomica import ErgonomicaError

def color(argc):
    """color: Easily print terminal color codes.

    Usage:
        color COLOR
        color bg COLOR
    """


    if argc.args['bg']:
        module = colorama.Back
    else:
        module = colorama.Fore
    try:
        return getattr(module, argc.args['COLOR'].upper())
    except AttributeError:
        raise ErgonomicaError("[ergo: color]: No such color '{}'.".format(argc.args['COLOR']))

    return


exports = {'color': color}


