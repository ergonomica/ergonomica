"""
[lib/lib/if.py]

Defines the Ergonomica if conditional construct.
"""

verbs = {}

def _if(argc):
    """FUNCTION1 FUNCTION2 ARGS,...@If FUNCTION1 is True, evaluates FUNCTION2 with ARGS."""
    if argc.ns[args[0]]:
        argc.ns[args[1])


verbs["if"] = _if
