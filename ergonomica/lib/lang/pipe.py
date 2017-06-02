#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/pipe.py]

The piping module.
"""

import os
from multiprocessing import Pool, cpu_count
from ergonomica.lib.lang.docopt import DocoptException
from ergonomica.lib.lang.arguments import ArgumentsContainer
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.arguments import get_typed_args

# initialize multiprocessing pool
POOL = Pool(cpu_count())

class Operation(object):
    """Defines an Operation object, holding a function and its arguments."""
    def __init__(self, function, arguments):
        self.function, self.arguments = function, arguments

class Pipeline(object):
    """Defines a pipeline object for redirecting the output of some functions to others."""

    # tokenized functions to be piped to
    operations = []
    args = []
    env = Environment()
    namespace = {}

    def __init__(self, env, namespace):
        """Initialize a Pipeline object."""
        self.env = env
        self.namespace = namespace

    def append_operation(self, operation):
        """Add an Operation type to the end of the Pipeline."""
        self.operations.append(operation)

    def stdout(self):
        """Evaluate the entire pipeline, giving the final output."""
        cur = []
        for operation in self.operations:
            if not callable(operation.function): # then call as shell command
                os.system("%s %s" % (operation.function, " ".join(operation.arguments)))

            else:
                # for some reason pylint thinks _operation and argv are undefined and/or unused
                _operation = operation
                argv = [str(x) for x in _operation.arguments] # pylint: disable=unused-variable
                try:

                    # it's pretty much impossible to shorten this
                    # pylint: disable=line-too-long, undefined-variable
                    current_op = lambda x, _operation=_operation, argv=argv: _operation.function(ArgumentsContainer(self.env,
                                                                                                                    self.namespace,
                                                                                                                    x,
                                                                                                                    get_typed_args(_operation.function.__doc__, argv)))
                except DocoptException as error:
                    return "[ergo: ArgumentError]: %s." % str(error)
                if cur == []:
                    cur = current_op(None)
                else:
                    cur = current_op(cur)
                    if cur is None:
                        cur = []
                    else:
                        cur = list(cur)

        self.operations = []
        self.args = []
        return cur
