#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/pipe.py]

Piping module.
"""

import os
from docopt import docopt, DocoptException
from ergonomica.lib.lang.arguments import ArgumentsContainer
from ergonomica.lib.lang.environment import Environment
from multiprocessing import Pool, cpu_count
from ergonomica.lib.lang.arguments import get_typed_args

# initialize multiprocessing pool
POOL = Pool(cpu_count())

class Operation:
    def __init__(self, f, args):
        self.f, self.args = f, args
        
class Pipeline:

    # tokenized functions to be piped to
    operations = []
    args = []
    env = Environment()
    ns = {}
    
    def __init__(self, env, ns):
        self.env = env
        self.ns = ns

    def append_operation(self, op):
        self.operations.append(op)
        
    def STDOUT(self):
        cur = []
        for operation in self.operations:
            if not callable(operation.f): # then call as shell command
                os.system("%s %s" % (operation.f, " ".join(operation.args)))
                    
            else:
                _operation = operation
                argv = [str(x) for x in _operation.args]
                try:
                    o = lambda x, _operation=_operation: _operation.f(ArgumentsContainer(self.env, self.ns, x, get_typed_args(_operation.f.__doc__, argv)))
                except DocoptException as e:
                    return "[ergo: ArgumentError]: %s." % str(e)
                if cur == []:
                    cur = o(None)
                else:
                    cur = [o(x) for x in cur]
                    
        self.operations = []
        self.args = []
        return cur
    
    #stderr
    def STDERR(self):
        pass
    
