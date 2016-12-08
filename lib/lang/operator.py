#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/operator.py]

The operator parser for Ergonomica. Defines get_operator, which returns the operator for a given
block of Ergonomica code (e.g., get_operator("(map) x + 3") returns "map").
"""

# pylint doesn't know that this file will be imported from ../../ergonomica
# pylint: disable=import-error

import re
import itertools

def get_operator(string):
    """Find functional-programming operators in a string.
       e.g., get_operator("(map) x + 3")       = "map"
             get_operator("(filter) x == '1'") = "filter".
    """
    try:
        return re.match(r"\([A-z]*\)", string.strip()).group()[1:-1]
    except AttributeError:
        return False


def run_operator(block, runtime):
    operator = get_operator(block)

    # (map) -- map an operator to a list of operands
    if operator == "map":
        func = eval("lambda x: " + block.replace("(map)", ""))
        runtime.lastlast_args = runtime.last_args
        runtime.last_args = map(func, runtime.last_args)
        return runtime.last_args

    # (filter) -- return all arguments that match the specified function
    elif operator == "filter":
        func = eval("lambda x: " + block.replace("(filter)", ""))
        runtime.lastlast_args = runtime.last_args
        runtime.last_args = [x for x in runtime.last_args if func(x)]
        return runtime.last_args

    # (match) -- return all arguments that match the specified regexp
    elif operator == "match":
        runtime.lastlast_args = runtime.last_args
        runtime.last_args = [x for x in runtime.last_args if re.match(block.replace("(match)", "").strip(), x)]
        return runtime.last_args

    # (reverse) -- reverse the order of all arguments
    elif operator == "reverse":
        runtime.lastlast_args = runtime.last_args
        runtime.last_args = runtime.last_args[::-1]
        return runtime.last_args

    # (splice) -- splice the last and 2nd last argument lists together
    elif operator == "splice":
        runtime.last_args = list(filter(None, sum(itertools.izip_longest(runtime.lastlast_args, runtime.last_args), ())))
        return runtime.last_args

    # (split) -- split input strings by spaces
    elif operator == "split":
        runtime.last_args = [item for sublist in [x.split() for x in runtime.last_args] for item in sublist]
        return runtime.last_args
        
    # (kwsplice) -- map the last and 2nd last argument lists into a dictionary
    elif operator == "kwsplice":
        runtime.lastlast_kwargs = runtime.last_kwargs
        runtime.last_kwargs = {runtime.last_args[i]:runtime.lastlast_args[i] for i in range(len(runtime.last_args))}
        return runtime.last_kwargs
    else:
        return False
