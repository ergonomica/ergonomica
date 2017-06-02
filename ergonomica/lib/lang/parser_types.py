"""
[lib/lang/parser_types.py]

Define types for the Ergonomica runtime/parser.
"""

from ergonomica.lib.lang.tokenizer import tokenize

def make_function(evaluator, function):
    """Return non-evaluated function object that will call the Ergonomica code in
    its body when invoked."""

    def function_object(argc):
        """An Ergonomica runtime function."""
        namespace = argc.ns
        for item in argc.args:
            namespace[item] = argc.args[item]
        return evaluator(function.body, namespace)

    function_object.__doc__ = "usage: function " + function.argspec[1:]
    return function_object

class Function(object):
    """Container for a generic user-defined Ergonomica function."""

    name = False
    body = []
    argspec = ""
    evaluator = lambda x: x

    def __init__(self, evaluator):
        self.evaluator = evaluator

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
        self.body[-1].type = "EOF"

        return {self.name: make_function(self.evaluator, self)}

class Command(object):
    """Container for Ergonomica commands being run."""

    def __init__(self):
        pass
