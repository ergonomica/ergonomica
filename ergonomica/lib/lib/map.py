"""
[lib/lib/map.py]

Defines the Ergonomica map command.
"""

from ergonomica.lib.lang.arguments import ArgumentsContainer
from docopt import docopt

verbs = {}

def _map(argc):
    """FUNCTION@"""
    function = argc.ns[argc.args["FUNCTION"]]
    docstring = "usage: function " + function.__doc__.split("@")[0]
    return function(ArgumentsContainer(argc.env, argc.ns, None, docopt(docstring, argv=[argc.stdin])))

verbs["map"] = _map
