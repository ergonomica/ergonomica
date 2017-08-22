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

def shuffle(array):
    array2 = [x for x in array]  # copy since arrays are mutable
    random.shuffle(array2)
    return array2

def accumulate(function, array):
    _accum = array[0]
    for i in array[1:]:
        _accum =  function(_accum, i)

    return _accum

def _slice(*args):
    if len(args) == 2:
        return args[0][args[1]]
    elif len(args) == 3:
        return args[0][args[1]:args[2]]

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
                  'and': lambda x, y: x and y,
                  'or': lambda x, y: x or y,
                  'nor': lambda x, y: not (x or y),
                  'nand': lambda x, y: not (x and y),
                  'xor': lambda x, y: (x or y) and (not (x and y)),
                  'len': len,
                  '=': lambda *x: len(set(x)) == 1,
                  '!=': lambda *x: not (len(set(x)) == 1),
                  'not': lambda x: not x,
                  '?file': os.path.isfile,
                  '?dir': os.path.isdir,
                  '?match': lambda x, y: re.match(x, y).group() if re.match(x, y) else None,
                  '?contains': lambda x, y: x in y,
                  'type': lambda x: type(x).__name__,
                  'pipe': pipe,
                  'first': lambda x: x[0],
                  'rest': lambda x: x[1:],
                  'list': lambda *x: list(x),
                  'split': lambda x, y: x.split(y),
                  'flatten': flatten,
                  'zip': lambda x, y: [x for l in zip(x, y) for x in l],
                  'filter': lambda op, arr: [x for x in arr if op(x)],                  
                  'accum': accumulate,
                  'apply': lambda f, args: f(*args),
                  'random': random.random(),
                  'randint': randint,
                  'randpick': random.choice,
                  'round': round,
                  'replace': re.sub,
                  'search': re.findall,
                  'shuffle': shuffle,
                  'str': str,
                  'int': int,
                  'float': float,
                  'count': lambda x, y: y.count(x),
                  'slice': _slice})


