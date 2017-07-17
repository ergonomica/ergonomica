#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/write.py]

Defines the "write" command.
"""


import types

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def flatten_stdin(stdin):
    if isinstance(stdin, types.GeneratorType):
        _sum = []
        for i in stdin:
            _sum += flatten_stdin(i)
        return _sum
    else:
        return stdin
        

def main(argc):
    """write: Write STDIN to file FILE.

    Usage:
        write <file>FILE
    """
    
    open(argc.args['FILE'], 'w').write('\n'.join(flatten([flatten_stdin(x) for x in argc.stdin])))
