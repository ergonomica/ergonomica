"""
[lib/lib/addstring.py]

Defines the Ergonomica addstring command.
"""


def _filter(argc):
    """filter: Filter items in STDIN.

    Usage:
        filter [INDICES...]
    """

    indices = argc.args['INDICES']
    for i in indices:
        yield argc.stdin[int(i)]


exports = {'filter': _filter}
