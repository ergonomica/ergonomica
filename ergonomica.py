#!/usr/bin/python
# pylint: disable=W0703
"""
[ergonomica.py]

The ergonomica runtime.
"""

import os
from multiprocessing import Process
from parser import tokenize
from verbs import verbs
from error_handler import cmd_check

HOME = os.getenv(key="HOME")
CMD_HIST = []

try:
    os.chdir(HOME + "/.ergo")
except OSError as e:
    os.mkdir(HOME + "/.ergo")
    print "Created directory ~/.ergo"
try:
    hist_file = open(HOME + "/.ergo/history.ergo_history", 'w+')
except IOError as e:
    print "An error occured while accessing file: " + str(e)

def ergo_run(stdin):
    """Evaluate ergonomica commands."""
    tokens = tokenize(stdin)
    f = lambda: verbs.verbs[tokens[0][0]](tokens[1], tokens[2])
    return Process(target=f)

while verbs.run:
    STDIN = raw_input("[ergo: %s}> " % (verbs.directory))
    STDOUT = []
    LAST = tokenize(STDIN.split("->")[0])[1]
    EXEC = len(STDIN.split("->"))
    try:
        EXEC -= 1
        #STDOUT = eval(STDIN)
        CMD_HIST.append(STDIN)
        BLOCKS = [tokenize(x) for x in STDIN.split("->")]
        for i in range(0, len(BLOCKS)):
            if (cmd_check(BLOCKS[i])):
                print cmd_check(BLOCKS[i])
                continue
            kwargs = {}
            STDOUT = verbs.verbs[BLOCKS[i][0][0]](LAST, {s.split(":")[0]:s.split(":")[1] for s in BLOCKS[i][2]})
            # filter out none
            STDOUT = [x for x in STDOUT if x != None]
    except IndexError, e:
        STDOUT = repr(e)
    print STDOUT
    if not isinstance(STDOUT, list):
        LAST = [STDOUT]
        if not EXEC:
            print STDOUT
    else:
        LAST = []
        print "STDOUT IS", STDOUT
        for item in STDOUT:
            for subitem in item:
                LAST.append(subitem)
                if not EXEC:
                    print subitem
                
