#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_uuid.py]

Defines the "uuid" command.
"""

import sys
import os
import random
from random_words import RandomWords

from ergonomica import ErgonomicaError
from ergonomica.lib.util.util import expand_path

def uuid(argc):
    """uuid: Yields a Universal Unique ID (UUID).

    Usage:
        uuid [int | hex | words] [LENGTH]
    """
    
    if not argc.args['LENGTH']:
        length = 4
    else:
        length = int(argc.args['LENGTH'])

        
    if argc.args['hex']:
        charset = '0123456789abcdef'
        return "".join([random.choice(charset) for x in range(length)])
    
    elif argc.args['words']:
        rw = RandomWords()
        return " ".join([str(x) for x in rw.random_words(count=length)])

    else:
        charset = "0123456789"
        return "".join([random.choice(charset) for x in range(length)])

        

exports = {'uuid': uuid}


