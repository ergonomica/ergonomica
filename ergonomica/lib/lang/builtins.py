#!/usr/bin/env python
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
        argv_read = False
        args = list(args) # so we can pop from it
        
        for i in argspec:
            if i.startswith("*"):
                if argv_read:
                    raise ErgonomicaError("[ergo: SyntaxError]: Multiple argv arguments.")
                else:
                    argv_read = True
                    self.update({i[1:]: args})
            else:
                self.update({i: args.pop()})

        self.outer = outer

    def find(self, var):
        return self if (var in self) else self.outer.find(var)

def randint(lower, upper=None):

    if not upper:
        lower, upper = 0, lower

    
    if not isinstance(lower, int):
        raise ErgonomicaError("[ergo: randint]: TypeError: '{}' not an integer.".format(str(lower)))
        
    elif not isinstance(upper, int):
        raise ErgonomicaError("[ergo: randint]: TypeError: '{}' not an integer.".format(str(upper)))
    

    return random.randint(lower, upper)

def flatten(arr):
    
    if not isinstance(arr, list):
        raise ErgonomicaError("[ergo: flatten]: Non-list passed.")
    
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
    if not isinstance(array, list):
        raise ErgonomicaError("[ergo: shuffle]: TypeError: Non-list passed.")
    
    array2 = [x for x in array]  # copy since arrays are mutable
    random.shuffle(array2)
    return array2

def accumulate(function, array):
    _accum = array[0]
    for i in array[1:]:
        _accum = function(_accum, i)
    return _accum

def _slice(*args):
    if len(args) == 2:
        if not isinstance(args[0], int):
            raise ErgonomicaError("[ergo: slice]: TypeError: Index '{}' not an integer.".format(str(args[0])))
        try:
            return args[1][args[0]]
        except IndexError:
            raise ErgonomicaError("[ergo: slice]: IndexError: Index {} out of range.".format(str(args[0])))
    elif len(args) == 3:
        if not isinstance(args[0], int):
            raise ErgonomicaError("[ergo: slice]: TypeError: Index '{}' not an integer.".format(str(args[0])))
        if not isinstance(args[1], int):
            raise ErgonomicaError("[ergo: slice]: TypeError: Index '{}' not an integer.".format(str(args[1])))

        return args[2][args[0]:args[1]]

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
namespace.update({'print': lambda *x: x[0] if len(x) == 1 else list(x),
                  'sleep': sleep,
                  '+': global_sum,
                  '-': lambda a, b: a - b,
                  '^': lambda a, b: a ** b,
                  '/': lambda a, b: a / b,
                  '%': lambda a, b:  b % a,
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
                  'finditem':lambda x, y: y.find(x),
                  'repr': lambda x: repr(x),
                  'repeat': lambda x, y, *argv: [y(*argv) for i in range(x)],
                  'reverse': lambda arr: arr[::-1],
                  'slice': _slice})
