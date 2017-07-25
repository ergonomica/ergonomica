"""
[lib/lib/if.py]

Defines the Ergonomica if conditional construct.
"""

from ergonomica.lib.lang.pipe import recursive_gen, flatten

def _if(argc):
    """if: If this, do that.

    Usage:
       if FUNCTION1 FUNCTION2 [FUNCTION3]
    """
    
    if flatten(recursive_gen(argc.ns[argc.args['FUNCTION1']]([])))[0]:
        return flatten(recursive_gen(argc.ns[argc.args['FUNCTION2']]([])))
    else:
        if argc.args['FUNCTION3']:
            return argc.ns[argc.args['FUNCTION3']]([])


exports = {'if': _if}
