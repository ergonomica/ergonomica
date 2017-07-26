"""
[lib/lib/not.py]

Defines the Ergonomica not conditional construct.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError

def _not(argc):
    """not: negate booleans.

    Usage:
        not [BOOL]
    """
    
    if argc.args['BOOL']:
        if argc.args['BOOL'] == "True":
            yield False
        elif argc.args['BOOL'] == "False":
            yield True
        else:    
            raise ErgonomicaError("[ergo: not]: '{}' not a boolean.".format(argc.args['BOOL']))
    else:
        for x in argc.stdin:
            if x == "True":
                yield False
            elif x == "False":
                yield True
            else:    
                raise ErgonomicaError("[ergo: not]: '{}' not a boolean.".format(x))


exports = {'not': _not}
