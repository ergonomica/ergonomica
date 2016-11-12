"""
[ergonomica.py]
The ergonomica runtime.
"""

import subprocess
from multiprocessing import Process

from lexer import tokenize
from verbs import verbs

def ergo_run(stdin, pipe=):
    """Evaluate ergonomica commands."""
    tokens = tokenize(stdin)
    f = lambda: verbs.verbs[tokens[0][0]](tokens[1], tokens[2])
    return Process(target = f)
    
while verbs.run:
    STDIN = raw_input("[ergo}> ").split("->")
    STDOUT = []
    try:
        for block in STDIN:
            parent_conn, child_conn = Pipe()
            e = ergo_run(block)
            e.start()
            STDOUT.append(ergo)
    except Exception, e:
        STDOUT = repr(e)
    print STDOUT
