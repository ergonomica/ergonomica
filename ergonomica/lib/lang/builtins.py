#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lang/stdlib.py]

Define the ErgonomicaError standard library.
"""

import re
import os
import random
from time import sleep
from ergonomica import ErgonomicaError

try:
    unicode
except NameError:
    unicode = str

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
        stdout = functions[0]()

        # force output to be an array---if there's one output, make it
        # an array with one item
        if not isinstance(stdout, list):
            return [stdout]
        else:
            return stdout

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

def array_equal(arr1, arr2):
    for i in arr1:
        if i not in arr2:
            return False
        elif arr1.count(i) != arr2.count(i):
            return False
    return True

def obj_set(arr, order=True):
    new_arr = []
    for i in arr:
        contained = False
        if not order:
            if not (isinstance(i, list) or isinstance(i, str) or isinstance(i, unicode)):
                raise ErgonomicaError("[ergo: ~=]: Non-iterable passed.")

        for j in new_arr:
            if order:
                if i == j:
                    if contained:
                        break
                    else:
                        contained = True

            else:
                if set(i) == set(j):
                    if contained:
                        break
                    else:
                        contained = True

        if not contained:
            new_arr.append(i)

    return new_arr

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
                  '*': lambda *arr: accumulate(lambda a, b: a * b, arr),
                  't': True,
                  'f': False,
                  'none': None,
                  'pi': 3.141592653589793,
                  'e': 2.718281828459045,
                  'j': 1j,
                  'max': lambda arr: max(arr),
                  'min': lambda arr: min(arr),
                  'and': lambda x, y: x and y,
                  'or': lambda x, y: x or y,
                  'nor': lambda x, y: not (x or y),
                  'nand': lambda x, y: not (x and y),
                  'xor': lambda x, y: (x or y) and (not (x and y)),
                  'len': len,
                  'unique': obj_set,
                  '=': lambda *x: len(obj_set(x)) == 1,
                  '~': lambda *x: len(obj_set(x, order=False)) == 1,
                  '!=': lambda *x: not (len(obj_set(x)) == 1),
                  'not': lambda x: not x,
                  '?file': lambda x: os.path.isfile(x) and (not (os.path.islink(x))),
                  '?dir': os.path.isdir,
                  '?link': os.path.islink,
                  '?match': lambda x, y: re.match(x, y).group() if re.match(x, y) else None,
                  '?contains': lambda x, y: x in y,
                  'type': lambda x: type(x).__name__,
                  'pipe': pipe,
                  'join': lambda x, y: x.join(y),
                  'first': lambda x: x[0],
                  'rest': lambda x: x[1:],
                  'list': lambda *x: list(x),
                  'split': lambda x, y: y.split(x),
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
                  'str': lambda x: str(x),
                  'int': lambda x: int(x),
                  'bool': lambda x: bool(x),
                  'float': lambda x: float(x),
                  'count': lambda x, y: y.count(x),
                  'repr': lambda x: repr(x),
                  'slice': _slice})




