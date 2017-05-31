"""
[lib/lib/map.py]

Defines the Ergonomica map command.
"""

from multiprocessing import Pool
from ergonomica.lib.lang.arguments import ArgumentsContainer, get_typed_args


def main(argc):
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

    # initialize multiprocessing pool for distributing map.
    pool = Pool(argc.env.cpu_count)

    operation = lambda x: function(ArgumentsContainer(argc.env,
                                                      argc.ns,
                                                      [],
                                                      get_typed_args(function.__doc__, x)))

    return list(pool.map(operation, args[1]))
