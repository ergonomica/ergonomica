"""
[lib/lib/map.py]

Defines the Ergonomica map command.
"""

import itertools
from ergonomica.lib.lang.arguments import ArgumentsContainer, get_typed_args


def main(argc):
    """
    map: Map an argument on STDIN.

    Usage:
       map ARGS...
       map -b BLOCKSIZE ARGS...

    Options:
       -i --ignore-blocksize  If the last block is not complete, ignore.
    """
    
    i = 0
    j = 0
    skip = 0
    f_args = argc.args['ARGS'][1:]
    args = [] # properly partitioned arguments
    mapped_function = argc.ns[argc.args['ARGS'][0]]
    argskip = int(argc.args['BLOCKSIZE']) if argc.args['-b'] else 0
    i -= argskip

    while i <= len(argc.stdin):

        if j == 0:
            if argskip:
                i += argskip
                j = i % len(f_args)
            else:
                i += skip
            if i >= len(argc.stdin):
                break
            skip = 0
            args.append([])


        if (f_args[j][0] == "{") and (f_args[j][-1] == "}"):
            try:
                if f_args[j] == "{}":
                    index = 0
                else:
                    index = int(f_args[j][1:-1])

                skip = index - 1 if index - 1 > skip else skip
                if i-j + index > len(argc.stdin):
                    break

                args[-1].append(argc.stdin[(i - j)  + index])
                j = (j+1) % len(f_args)
                i += 1

            except ValueError:
                raise Exception(("[ergo: map]: Error processing argument substitution '{sub}'. "
                                 "Should only be an integer (i.e. of the form \\d+).")
                                .format(sub=f_args[j][1:-1]))

        else:
            args[-1].append(f_args[j])
            j = (j+1) % len(f_args)


    args = [ArgumentsContainer(argc.env,
                               argc.ns,
                               [],
                               get_typed_args(mapped_function.__doc__, x)) for x in args]


    return list(itertools.chain.from_iterable(map(mapped_function, args)))
