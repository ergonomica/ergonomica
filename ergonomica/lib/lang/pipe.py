#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/pipe.py]

Piping module.
"""

import sh
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
        cur = self.operations[0].args
        for operation in self.operations:
            if isinstance(operation.f, unicode): # then call as shell command
                try:
                    cur = getattr(sh, operation.f)(operation.args, _in = cur)
                except sh.ErrorReturnCode_1, e:
                    cur = e
                    
            else:
                _operation = operation
                argv = _operation.args
                try:
                    o = lambda x, _operation=_operation: _operation.f(ArgumentsContainer(self.env, self.ns, x, get_typed_args(_operation.f.__doc__, argv)))
                except DocoptException as e:
                    return "[ergo: ArgumentError]: %s." % str(e)
                if cur == []:
                    cur = o(None)
                else:
                    cur = list(map(o, cur))
    
        self.operations = []
        self.args = []
        return cur
    
    #stderr
    def STDERR(self):
        pass
    
    
#class AsyncPipeline(Pipeline):
    
