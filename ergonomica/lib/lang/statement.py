#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/statement.py]

The statement parser for Ergonomica. Defines get_statement, which returns the statement for a given
block of Ergonomica code (e.g., get_statement("run skynet.ergo") returns "run").
"""


def get_statement(string):
    """
    Find statement in a string.
    e.g., get_statement("import exports")    = "import"
          get_statement("run make_pie.ergo") = "filter".
    """

    statements = ["run", "import", "if", "for", "while"]

    for statement in statements:
        if string.startswith(statement + " "):
            return statement
    return ""
