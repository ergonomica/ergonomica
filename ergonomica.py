#!/usr/bin/python
# pylint: disable=W0703
"""
[ergonomica.py]
The ergonomica runtime.
"""

import os
import sys
import subprocess
from multiprocessing import Process
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

def ergo_run(stdin):
    """Evaluate ergonomica commands."""
    tokens = tokenize(stdin)
    f = lambda: verbs.verbs[tokens[0][0]](tokens[1], tokens[2])
    return Process(target = f)

while verbs.run:
    STDIN = raw_input("[ergo}> ")
    STDOUT = []
    try:
        STDOUT = eval(STDIN)
        CMD_HIST.append(STDIN)
        blocks = [tokenize(x) for x in STDIN.split("->")]
        for i in range(0, len(blocks)):
            kwargs = {}
            blocks[i] = verbs.verbs[blocks[i][0][0]](blocks[i][1], {s.split(":")[0]:s.split(":")[1] for s in blocks[i][2]})
            STDOUT = blocks
            # filter out none
            STDOUT = [x for x in STDOUT if x != None]
    except Exception, e:
        STDOUT = repr(e)
    for item in STDOUT:
        print item
