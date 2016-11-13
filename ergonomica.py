#!/usr/bin/python
# pylint: disable=W0703
"""
[ergonomica.py]

The ergonomica runtime.
"""

import os, sys, subprocess, readline
from multiprocessing import Process
from parser import tokenize
from verbs import verbs

CMD_HIST = []

try:
    os.chdir(verbs.home + "/.ergo")
except OSError as e:
    os.mkdir(verbs.home + "/.ergo")
    print "Created directory ~/.ergo"
try:
    hist_file = open(verbs.home + "/.ergo/history.ergo_history", 'w+')
except IOError as e:
    print "An error occured while accessing file: " + str(e)

def ergo_run(stdin):
    """Evaluate ergonomica commands."""
    tokens = tokenize(stdin)
    f = lambda: verbs.verbs[tokens[0][0]](tokens[1], tokens[2])
    return Process(target=f)

while verbs.run:
    STDIN = raw_input("[ergo: %s in %s}> " % (verbs.user, verbs.directory))
    STDOUT = []
    try:
        #STDOUT = eval(STDIN)
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
        print STDOUT
    if not isinstance(STDOUT, list):
        print STDOUT
    else:
        for item in STDOUT:
            for subitem in item:
                print subitem
