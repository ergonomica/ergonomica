"""
[lib/lib/map.py]

Defines the Ergonomica map command.
"""

from __future__ import print_function
import itertools
import subprocess
from ergonomica.lib.lang.arguments import ArgumentsContainer, get_typed_args

def main(argc):
    """
    map: Map an argument on STDIN.

    Usage:
        map ARGS...
        map -b BLOCKSIZE ARGS...

    Options:
        -i --ignore-blocksize  If the last block is not complete, ignore.
    
    Examples:
        ls | map rm {}             # Remove all files in the current directory
        print 1 1 1 | map print {} # re-prints out [1,1,1]
        => 1
           1
           1
    """

    i = 0
    j = 0
    skip = 0
    f_args = argc.args['ARGS'][1:]
    try:
        mapped_function = argc.ns[argc.args['ARGS'][0]]
    except KeyError:
        #subprocess.check_output()
        mapped_function = lambda x: [subprocess.check_output([argc.args['ARGS'][0]] + x.args)[:-1]]

    blocksize = 1
    for i in f_args:
        if i.startswith("{") and i.endswith("}"):
            try:
                blocksize = int(i[1:-1]) + 1 if int(i[1:-1]) + 1 > blocksize else blocksize
            except ValueError:
                pass

    processed_args = []

    # pylint: disable=consider-using-enumerate
    for i in range(0, len(argc.stdin), blocksize):
        args = []
        for j in range(len(f_args)):
            if f_args[j].startswith("{") and f_args[j].endswith("}"):
                if f_args[j] == "{}":
                    args.append(argc.stdin[i])
                else:
                    args.append(argc.stdin[int(f_args[j][1:-1]) + i])
            else:
                args.append(f_args[j])

        if mapped_function.__doc__:
            processed_args.append(ArgumentsContainer(argc.env,
                                         argc.ns,
                                         [],
                                         get_typed_args(mapped_function.__doc__, args)))
        else:
            processed_args.append(ArgumentsContainer(argc.env,
                                         argc.ns,
                                         [],
                                         args))

    return list(itertools.chain.from_iterable(map(mapped_function, processed_args)))
