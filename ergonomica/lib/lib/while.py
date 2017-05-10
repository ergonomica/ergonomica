"""
[lib/lib/while.py]

Defines the Ergonomica while loop construct.
"""

verbs = {}

def _while(env, args):
    """FUNCTION1 FUNCTION2 ARGS,...@While FUNCTION1 is True, evaluates FUNCTION2 with ARGS."""
    while env.verbs[args[0]]:
        env.verbs[args[1]](args[2:])


verbs["while"] = _while
