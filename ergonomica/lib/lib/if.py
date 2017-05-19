"""
[lib/lib/if.py]

Defines the Ergonomica if conditional construct.
"""

verbs = {}

def _if(argc):
    """if: If this, do that.

    Usage:
       if FUNCTION1 FUNCTION2
    """
    if argc.ns[argc.args['FUNCTION1']](argc):
        return argc.ns[argc.args['FUNCTION2']](argc)

verbs["if"] = _if
