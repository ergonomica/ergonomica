#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/pipe.py]

Piping module.
"""

from docopt import docopt

from ergonomica.lib.lang.arguments import ArgumentsContainer
from ergonomica.lib.lang.environment import Environment
from multiprocessing import Pool, cpu_count

# initialize multiprocessing pool
p = Pool(cpu_count())

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
            _operation = operation
            o = lambda x, _operation=_operation: _operation.f(ArgumentsContainer(self.env, self.ns, x, docopt("usage: function " + _operation.f.__doc__.split("@")[0], argv=_operation.args)))
            cur = list(map(o, cur))
        return cur
    
    #stderr
    def STDERR(self):
        pass
    
    
#class AsyncPipeline(Pipeline):

