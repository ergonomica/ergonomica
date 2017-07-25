"""
[lib/lib/ergo_replace.py]

Defines the Ergonomica replace command.
"""

import re

def replace(argc):
    """replace: Replace regexp match in STDIN.

    Usage:
       replace REGEXP SUB
    """
    
    return [re.sub(argc.args['REGEXP'], argc.args['SUB'], x) for x in argc.stdin]
    

exports = {'replace': replace}
