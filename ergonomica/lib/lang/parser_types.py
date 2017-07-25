"""
[lib/lang/parser_types.py]

Define types for the Ergonomica runtime/parser.
"""

import json
from ergonomica.lib.lang.tokenizer import tokenize
from ergonomica.lib.lang.pipe import flatten, recursive_gen

def make_function(evaluator, body, argspec):
    """Return non-evaluated function object that will call the Ergonomica code in
    its body when invoked."""

    def function_object(argc):
        """An Ergonomica runtime function."""
        namespace = argc.ns
        for item in argc.args:
            namespace[str(item)] = argc.args[item]
        return flatten(recursive_gen(evaluator(body, namespace)))

    function_object.__doc__ = "usage: function " + argspec[1:]
    return function_object

class Function(object):
    """Container for a generic user-defined Ergonomica function."""

    name = False
    body = []
    argspec = ""
    evaluator = lambda x: x

    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.body = []

    def set_name(self, string):
        """Set the name of a Function object."""
        self.name = string

    def append_to_body(self, token):
        """Append an token to the function's body."""
        if not self.body:
            self.body = [token]
        else:
            self.body.append(token)

    def make(self):
        """Return an (unevaluated) function that acts as an Ergonomica builtin function."""
        # add EOF character to end of function
        self.body.append(tokenize("\n")[0])
        #self.body[-1].type = "EOF"

        return {self.name: make_function(self.evaluator, self.body, self.argspec)}

class Command(object):
    """Container for Ergonomica commands being run."""

    def __init__(self):
        pass
