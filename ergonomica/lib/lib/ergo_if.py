"""
[lib/lib/if.py]

Defines the Ergonomica if conditional construct.
"""


def main(argc):
    """if: If this, do that.

    Usage:
       if FUNCTION1 FUNCTION2 [FUNCTION3]
    """
    if argc.ns[argc.args['FUNCTION1']](argc):
        return argc.ns[argc.args['FUNCTION2']](argc)
    else:
        return argc.ns[argc.args['FUNCTION3']](argc)
