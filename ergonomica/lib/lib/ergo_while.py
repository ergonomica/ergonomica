"""
[lib/lib/while.py]

Defines the Ergonomica while loop construct.
"""

from time import sleep


def ergo_while(argc):
    """while: While CONDITION returns true, do BODY.

    Usage:
        while [-s <int>SLEEP] CONDITION BODY

    Options:
        -s  Sleep for SLEEP seconds before iterating again.       
    """

    if argc.args['-s']:
        while env.ns[args[0]]:
            time.sleep(argc.args['SLEEP'])
            env.ns[args[1]](args[2:])

    else:
        while env.ns[args[0]]:
            env.ns[args[1]](args[2:])
