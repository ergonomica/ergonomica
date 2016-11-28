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

from lib.lang.error import ErgonomicaError

def get_operator(string):
    """Find functional-programming operators in a string.
       e.g., get_operator("(map) x + 3")       = "map"
             get_operator("(filter) x == '1'") = "filter".
    """
    operators = ["map", "filter", "match", "reverse", "splice", "kwsplice", "decompose"]
    try:
        operator = re.match(r"\([A-z]*\)", string.strip()).group()[1:-1]
        if operator in operators:
            return operator
        else:
            raise ErgonomicaError("No such operator %s" % operator)
    except AttributeError:
        return False
