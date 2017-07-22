"""
[lib/lib/addstring.py]

Defines the Ergonomica addstring command.
"""


def main(argc):
    """filter: Filter items in STDIN.

    Usage:
        filter [INDICES...]
    """

    indices = argc.args['INDICES']
    for i in indices:
        yield argc.stdin[int(i)]
