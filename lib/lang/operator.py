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

operators = ["map" ,"filter", "match", "reverse", "splice", "split", "kw"]
    
def run_operator(block, pipe):
    operator = get_operator(block)

    # (map) -- map an operator to a list of operands
    if operator == "map":
        func = eval("lambda x: " + block.replace("(map)", ""))
        pipe.setstack_args([x for x in map(func, pipe.getstack_args(-1))])
        return pipe.args[-1]

    # (filter) -- return all arguments that match the specified function
    elif operator == "filter":
        func = eval("lambda x: " + block.replace("(filter)", ""))
        pipe.lastlast_args = pipe.getstack_args(-1)
        pipe.setstack_args([x for x in pipe.getstack_args(-1) if func(x)])
        return pipe.getstack_args(-1)

    # (match) -- return all arguments that match the specified regexp
    elif operator == "match":
        exp = block.replace("(match)", "").strip()
        pipe.setstack_args([x for x in pipe.getstack_args(-1) if re.match(exp, x.strip())])
        return pipe.getstack_args(-1)

    # (reverse) -- reverse the order of all arguments
    elif operator == "reverse":
        pipe.setstack_args(pipe.getstack_args(-1)[::-1])
        return pipe.getstack_args(-1)

    # (splice) -- splice the last and 2nd last argument lists together
    elif operator == "splice":
        pipe.setstack_args(list(filter(None, sum(itertools.izip_longest(pipe.getstack_args(-2), pipe.getstack_args(-1)), ()))))
        return pipe.getstack_args(-1)

    # (split) -- split input strings by spaces
    elif operator == "split":
        pipe.setstack_args([item for sublist in [x.split() for x in pipe.getstack_args(-1)] for item in sublist])
        return pipe.getstack_args(-1)
        
    # (kw) -- map the last and 2nd last argument lists into a dictionary
    elif operator == "kw":
        pipe.setstack_kwargs({pipe.getstack_args(-1)[i]:pipe.getstack_args(-1)[i+1] for i in range(len(pipe.getstack_args(-1)) - 1)})
        return pipe.getstack_kwargs(-1)
    else:
        return False
