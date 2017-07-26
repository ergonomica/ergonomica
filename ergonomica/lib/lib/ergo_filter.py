"""
[lib/lib/filter.py]

Defines the Ergonomica filter command.
"""

from ergonomica.lib.lang.exceptions import ErgonomicaError


def _filter(argc):
    """filter: Filter items in STDIN.

    Usage:
        filter [-n] [INDICES...]
    """

    try:
        indices = [int(x) for x in argc.args['INDICES']]
    except TypeError:
        # TODO: make this tell the user which index was a non-integer and potentially index of the faulty index
        raise ErgonomicaError("[ergo: filter]: Non-integer indices provided.")
    if argc.args['-n']:
        result = []
        for i in range(len(argc.stdin)):
            if i not in indices:
                result.append(argc.stdin[i])
        return result

    else:
        return [argc.stdin[int(i)] for i in indices]


exports = {'filter': _filter}
