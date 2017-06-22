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
 
    Usage:
       map ARGS...
       map -b BLOCKSIZE ARGS...

    Options:
       -i --ignore-blocksize  If the last block is not complete, ignore.
    """

    #global shared_argc
    #global shared_function

    shared_argc = argc
    
    i = 0
    j = 0
    skip = 0
    f_args = argc.args['ARGS'][1:]
    args = [] # properly partitioned arguments
    shared_function = argc.ns[argc.args['ARGS'][0]]
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
                    # if argc.args['--ignore-blocksize']:
                    #     break
                    # else:
                    #     raise Exception("[ergo: map]: [BlockSizeError]: Error partitioning STDIN into chunks of specified size. Use the --ignore-blocksize option to ignore any remaining parts.")

                    
                args[-1].append(argc.stdin[(i - j)  + index])
                j = (j+1) % len(f_args)
                i += 1
                
            except TypeError:
                raise Exception("[ergo: map]: Error processing argument substitution '%s'. Should be of the form {\d+}." % (item[1:-1]))
            
        else:
            args[-1].append(f_args[j])
            j = (j+1) % len(f_args)

    result = [shared_function(ArgumentsContainer(shared_argc.env,
                                               shared_argc.ns,
                                               [],
                                               get_typed_args(shared_function.__doc__, x))) for x in args]

    summed_result = []
    for item in result:
        summed_result += item

    return summed_result
    
    # initialize multiprocessing pool for distributing map.
    #pool = Pool(argc.env.cpu_count)

    #return list(itertools.chain.from_iterable(pool.map(map_operation, args[1])))
