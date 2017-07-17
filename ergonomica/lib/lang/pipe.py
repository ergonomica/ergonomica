#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/pipe.py]

The piping module.
"""

import os
import subprocess
from multiprocessing import Pool, cpu_count
from ergonomica.lib.lang.docopt import DocoptException
from ergonomica.lib.lang.arguments import ArgumentsContainer
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.arguments import get_typed_args
import types


# for escaping shell commands
try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote

# initialize multiprocessing pool
POOL = Pool(cpu_count())

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def flatten_stdin(stdin):
    if isinstance(stdin, types.GeneratorType):
        _sum = []
        for i in stdin:
            _sum += flatten_stdin(i)
        return _sum
    else:
        return stdin

class Operation(object):
    """Defines an Operation object, holding a function and its arguments."""
    def __init__(self, function, arguments):
        self.function, self.arguments = function, arguments

def operation_traverse(stdin, operations):
    if operations == []:
        yield [stdin]

    else:
        op = operations.pop()
        if stdin:
            for i in stdin:
                s = operation_traverse(i, operations)
                yield op([x for x in s])
        else:
            s = operation_traverse(None, operations)
            yield op([x for x in s])

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
        operations = []
        
        for operation in self.operations:
            
            # for some reason pylint thinks _operation and argv are undefined and/or unused
            _operation = operation
            argv = [str(x) for x in _operation.arguments] # pylint: disable=unused-variable
        
            if not callable(operation.function): # then call as shell command
                if len(self.operations) > 1:
                    operations.append(lambda x, _operation=_operation, argv=argv: subprocess.check_output([_operation.function] + [quote(x) for x in argv]))
                else:
                    def os_wrapper(_operation, argv):
                        os.system("{} {}".format(_operation.function, " ".join([quote(x) for x in argv])))
                        yield None
    
                    operations.append(lambda x, _operation=_operation, argv=argv: os_wrapper(_operation, argv))
            else:
                try:

                    # it's pretty much impossible to shorten this
                    # pylint: disable=undefined-variable
                    operations.append(lambda x, _operation=_operation, argv=argv: _operation.function(ArgumentsContainer(self.env,
                                                                                                                         self.namespace,
                                                                                                                         flatten([flatten_stdin(y) for y in x[0]]),
                                                                                                                         get_typed_args(_operation.function.__doc__, argv))))
                except DocoptException as error:
                    return "[ergo: ArgumentError]: %s." % str(error)

        
        
        # reverse the order of operations because operations will be popped from the stack
        # operations.reverse()
        
        self.operations = []
        self.args = []
        
        return operation_traverse(None, operations)

