#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lang/stdlib.py]

Define the ErgonomicaError standard library.
"""

import re
import os
import random
from time import sleep

class Namespace(dict):
    def __init__(self, argspec=(), args=(), outer=None):
        self.update(zip(argspec, args))
        self.outer = outer
    
    def find(self, var):
        return self if (var in self) else self.outer.find(var)

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

        if bs == 0:
            return f(pipe(blocksizes, *functions))
        else:
            return [f(arr) for arr in split_with_remainder(pipe(blocksizes, *functions), bs)]

def randint(lower, upper=None):
    if not upper:
        lower, upper = 0, lower

    return random.randint(lower, upper)

def flatten(arr):
    out = []
    for i in arr:
        if isinstance(i, list):
            out += flatten(i)
        else:
            out.append(i)
    return out

def global_sum(*arguments):
    """
    Return the sum of all arguments, regardless of their type.
    """

    _sum = arguments[0]
    for i in arguments[1:]:
        _sum += i
    return _sum


namespace = Namespace()
namespace.update({'print': lambda *x: x[0] if len(x) == 1 else x,
                  'sleep': sleep,
                  '+': global_sum,
                  '-': lambda a, b: a - b,
                  '^': lambda a, b: a ** b,
                  '/': lambda a, b: a / b,
                  '<=': lambda a, b: a <= b,
                  '<': lambda a, b: a < b,
                  '>': lambda a, b: a > b,
                  '>=': lambda a, b: a >= b,
                  '*': lambda a, b: a * b,
                  '#t': True,
                  '#f': False,
                  '#none': None,
                  '#pi': 3.141592653589793,
                  '#e': 2.718281828459045,
                  '#j': 1j,
                  '=': lambda *x: len(set(x)) == 1,
                  '!=': lambda *x: not (len(set(x)) == 1),
                  'not': lambda x: not x,
                  '?file': os.path.isfile,
                  '?dir': os.path.isdir,
                  '?match': lambda x, y: re.match(x, y).group() if re.match(x, y) else False,
                  'type': lambda x: type(x).__name__,
                  'pipe': pipe,
                  'first': lambda x: x[0],
                  'rest': lambda x: x[1:],
                  'list': lambda *x: list(x),
                  'split': lambda x, y: x.split(y),
                  'flatten': flatten,
                  'zip': lambda x, y: [x for l in zip(x, y) for x in l],
                  'apply': lambda f, args: f(*args),
                  'random': random.random(),
                  'randint': randint,
                  'randpick': random.choice,
                  'round': round,
                  'replace': re.sub,
                  'search': re.findall})


