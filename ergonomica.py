#!/usr/bin/python
# pylint: disable=W0703
"""
[ergonomica.py]
The ergonomica runtime.
"""

import os
import sys
from lexer import tokenize
from verbs import verbs

HOME = os.getenv(key="HOME")
CMD_HIST = []

try:
    os.chdir(HOME + "/.ergo")
except OSError as e:
    os.mkdir(HOME + "/.ergo")
    print "Created directory ~/.ergo"

hist_file = open("~/.ergo/history.ergo_history", 'w+')

def eval(stdin):
    """Evaluates the command"""
    tokens = tokenize(stdin)
    return verbs.verbs[tokens[0][0]](tokens[1], tokens[2])

while verbs.run:
    STDIN = raw_input("[ergo}> ")
    try:
        STDOUT = eval(STDIN)
        CMD_HIST.append(STDIN)
    except Exception, e:
        STDOUT = repr(e)
    print STDOUT
