#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/stdlib.py]

Define the ErgonomicaError standard library.
"""

class Namespace(dict):
    def __init__(self, argspec=(), args=(), outer=None):
        self.update(zip(argspec, args))
        self.outer = outer
    
    def find(self, var):
        return self if (var in self) else self.outer.find(var)


def global_sum(*arguments):
    """
    Return the sum of all arguments, regardless of their type.
    """
    
    _sum = arguments[0]
    for i in arguments[1:]:
        _sum += i
    return _sum

def split_with_remainder(array, bs):
    new_arrays = [[]]
    for a in array:
        if len(new_arrays[-1]) < bs:
            new_arrays[-1].append(a)
        else:
            new_arrays.append([a])
    return new_arrays

def pipe(blocksizes, *functions):
    blocksizes = list(blocksizes)
    functions = list(functions)
    if len(functions) == 1:
        return functions[0]()
    else:
        bs = blocksizes.pop()
        f = functions.pop()
        # # if (stdin == []) and (not (bs == 0)):
        # #     raise Exception

        if bs == 0:
            return f(pipe(blocksizes, *functions))
        else:
            return [f(arr) for arr in split_with_remainder(pipe(blocksizes, *functions), bs)]
        
    
namespace = Namespace()
namespace.update({'print': lambda *x: x,
                  '+': global_sum,
                  '-': lambda a, b: a - b,
                  '^': lambda a, b: a ** b,
                  '/': lambda a, b: a / b,
                  '<=': lambda a, b: a <= b,
                  '*': lambda a, b: a * b,
                  '#t': True,
                  '#f': False,
                  '=': lambda *x: len(set(x)) == 1,
                  '!=': lambda *x: not (len(set(x)) == 1),
                  'type': lambda x: type(x).__name__,
                  'pipe': lambda blocksizes, *functions: pipe(blocksizes, *functions),
                  'first': lambda x: x[0],
                  'rest': lambda x: x[1:],
                  'list': lambda *x: list(x)})


