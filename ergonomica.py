"""
[ergonomica.py]
The ergonomica runtime.
"""

import subprocess
from multiprocessing import Process
import readline

from parser import tokenize
from verbs import verbs

def ergo_run(stdin):
    """Evaluate ergonomica commands."""
    tokens = tokenize(stdin)
    f = lambda: verbs.verbs[tokens[0][0]](tokens[1], tokens[2])
    return Process(target = f)

while verbs.run:
    STDIN = raw_input("[ergo}> ")
    STDOUT = []
    try:
        blocks = [tokenize(x) for x in STDIN.split("->")]
        for i in range(0, len(blocks)):
            kwargs = {}
            blocks[i] = verbs.verbs[blocks[i][0][0]](blocks[i][1], {s.split(":")[0]:s.split(":")[1] for s in blocks[i][2]})
            STDOUT = blocks
            # filter out none
            STDOUT = [x for x in STDOUT if x != None]
    except Exception, e:
        STDOUT = repr(e)
    if not isinstance(STDOUT, list):
        print STDOUT
    else:
        for item in STDOUT:
            print item
