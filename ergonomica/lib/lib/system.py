#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/system.py]

Defines the "system" command.
"""

import os
import shlex
from subprocess import Popen, PIPE

verbs = {}

def system(argc):
    """STRING@"""
    output, err = Popen(shlex.split(argc.args["STRING"]), stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
    return output

verbs['sys'] = system
