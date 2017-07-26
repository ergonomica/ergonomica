"""
[lib/lib/ergo_join.py]

Defines the Ergonomica join command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError


def join(argc):
    """join: Join STDIN and argument array.
    
    Usage:
        join [-r] ARGS...
    """

    if argc.args['-r']:
        return argc.args['ARGS'] + argc.stdin
    else:
        return argc.stdin + argc.args['ARGS']


exports = {'join': join}
