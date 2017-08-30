#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[lib/lang/arguments.py]

The Ergonomica arguments handler. Creates the ArgumentsContainer object.
"""

import re
# this is querying the system docopt, not the docopt.py in this directory
from docopt import docopt # pylint: disable=relative-import


class ArgumentsContainer(object):
    """
    Defines a container to hold arguments to pass to functions. Contains
    various things accessible to functions such as:
    - Environment (current directory, prompt, etc.)
    - Namespace (holds all Ergonomica functions)
    - STDIN (data piped to the function)
    """
    # this is the standard (ns as namespace)
    def __init__(self, env, ns, args): # pylint: disable=invalid-name
        self.env, self.ns, self.args = env, ns, args # pylint: disable=invalid-name


def get_typed_args(docstring, argv, escape_dashes=True):
    """Given a function's docstring and the arguments passed:
    - Parses arguments using docopt
    - Converts them to desired types (based on docstring type declarations)"""

    # remove all type declarations
    docstring = re.sub("<.*?>", '', docstring)

    # read in docopt arguments
    if escape_dashes:
        d_parsed = docopt(docstring, argv=["\x00" + x for x in argv])
    else:
        d_parsed = docopt(docstring, argv=argv)

    # perform type modifications
    for item in re.findall("<[a-z]+>[A-Z]+", docstring):
        item = item[1:]
        _type, variable = item.split(">")[0]
        if _type == "str":
            pass
        else:
            evalable = True
            try:
                evaled_var = eval(d_parsed[variable])
            # ergonomica is supposed to return a string when the variable
            # isn't evalable--no conditions on specific error
            except:  # pylint: disable=bare-except
                evalable = False
            if (type(evaled_var).__name__ == _type) and evalable:
                d_parsed[variable] = evaled_var
            else:
                print("[ergo: TypeError]: Error converting '%s' to type '%s'.")

    return d_parsed


