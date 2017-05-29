"""
[lib/lib/map.py]

Defines the Ergonomica map command.
"""

from ergonomica.lib.lang.arguments import ArgumentsContainer, get_typed_args
from multiprocessing import Pool
from docopt import docopt


def ergo_map(argc):
    """
    map: Map an argument on STDIN.
    Map is passed a function name as well as a series of arguments 
    
    Usage:
       map ARGS...
       map -b BLOCKSIZE ARGS...

    Options:

    """    

    args = argc.args['ARGS']
    function = argc.ns[args[0]]
    if args.count("{}") > 1:
        print("[ergo]: [map]: Too many {} substitutions.")
    else:
        args = [argc.stdin if x == '{}' else x for x in args]

    out = []

    # initialize multiprocessing pool for distributing map.
    p = Pool(argc.env.cpu_count)

    o = lambda x: function(ArgumentsContainer(argc.env, argc.ns, None, get_typed_args(function.__doc__, x)))
    
    return list(map(o, args[1]))

