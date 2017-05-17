"""
[lib/lib/if.py]

Defines the Ergonomica if conditional construct.
"""

verbs = {}

def _if(argc):
    """FUNCTION1 FUNCTION2@If FUNCTION1 is True, evaluates FUNCTION2 with ARGS."""
    if argc.ns[argc.args['FUNCTION1']](argc):
        argc.ns[argc.args['FUNCTION2']](argc)


verbs["if"] = _if
