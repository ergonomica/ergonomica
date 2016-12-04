#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/operator.py]

The operator parser for Ergonomica. Defines get_operator, which returns the operator for a given
block of Ergonomica code (e.g., get_operator("(map) x + 3") returns "map").
"""


def get_statement(string):
    """Find functional-programming operators in a string.
       e.g., get_operator("(map) x + 3")       = "map"
             get_operator("(filter) x == '1'") = "filter".
    """

    statements = ["run", "import", "set"]

    for statement in statements:
        if string.startswith(statement):
            return statement
    return False
