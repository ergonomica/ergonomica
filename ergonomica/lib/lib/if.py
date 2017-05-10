"""
[lib/lib/if.py]

Defines the Ergonomica if conditional construct.
"""

verbs = {}

def _if(env, args):
    """FUNCTION1 FUNCTION2 ARGS,...@If FUNCTION1 is True, evaluates FUNCTION2 with ARGS."""
    if env.verbs[args[0]]:
        env.verbs[args[1]](args[2:])


verbs["if"] = _if
