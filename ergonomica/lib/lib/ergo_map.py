"""
[lib/lib/map.py]

Defines the Ergonomica map command.
"""

# global needed for sharing variables to multiple processes
# pylint: disable=global-statement

import itertools
from multiprocessing import Pool
from ergonomica.lib.lang.arguments import ArgumentsContainer, get_typed_args

# should match what's used inside functions
# pylint: disable=invalid-name

shared_argc = []
shared_function = lambda x: x

def map_operation(x):
    """An arbitrary mapped function."""

    global shared_argc
    global shared_function

    return shared_function(ArgumentsContainer(shared_argc.env,
                                              shared_argc.ns,
                                              [],
                                              get_typed_args(shared_function.__doc__, x)))


def main(argc):
    """
    map: Map an argument on STDIN.
    Map is passed a function name as well as a series of arguments

    Usage:
       map ARGS...
       map -b BLOCKSIZE ARGS...

    Options:

    """

    global shared_argc
    global shared_function

    shared_argc = argc

    args = argc.args['ARGS']
    shared_function = argc.ns[args[0]]
    if args.count("{}") > 1:
        print("[ergo]: [map]: Too many {} substitutions.")
    else:
        args = [argc.stdin if x == '{}' else x for x in args]

    # initialize multiprocessing pool for distributing map.
    pool = Pool(argc.env.cpu_count)

    return list(itertools.chain.from_iterable(pool.map(map_operation, args[1])))
