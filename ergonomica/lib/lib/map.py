"""
[lib/lib/map.py]

Defines the Ergonomica map command.
"""

from ergonomica.lib.lang.arguments import ArgumentsContainer, get_typed_args
from docopt import docopt

verbs = {}

def _map(argc):
    """
    map: STDIN to arguments.
    
    Usage:
       map ARGS...
    """    

    args = argc.args['ARGS']
    function = argc.ns[args[0]]
    if args.count("{}") > 1:
        print("[ergo]: [map]: Too many {} substitutions.")
    else:
        args = [argc.stdin if x == '{}' else x for x in args]
    return function(ArgumentsContainer(argc.env, argc.ns, None, get_typed_args(function.__doc__, args[1:])))

verbs["map"] = _map
