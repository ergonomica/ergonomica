"""
[lib/lib/contains.py]

Defines the Ergonomica contains command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError


def contains(argc):
    """contains: Check for existence of items in array.
    
    Usage:
        contains ITEMS...
    """
    
    for x in argc.args['ITEMS']:
        if x not in argc.stdin:
            return False
    return True


exports = {'contains': contains}
