"""
[lib/lib/if.py]

Defines the Ergonomica if conditional construct.
"""

from ergonomica.lib.lang.arguments import ArgumentsContainer
from ergonomica.lib.lang.pipe import recursive_gen, flatten

def _if(argc):
    """if: If this, do that.

    Usage:
       if FUNCTION1 FUNCTION2 [FUNCTION3]
    """
    new_argc = ArgumentsContainer(argc.env,
                                         argc.ns,
                                         [],
                                         {})
    
    if flatten(recursive_gen(argc.ns[argc.args['FUNCTION1']](new_argc)))[0]:
        return flatten(recursive_gen(argc.ns[argc.args['FUNCTION2']](new_argc)))
    else:
        if argc.args['FUNCTION3']:
            return argc.ns[argc.args['FUNCTION3']](new_argc)


exports = {'if': _if}
