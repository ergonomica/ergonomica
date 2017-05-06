#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[ergo.py]

The main Ergonomica runtime.
"""

import sys
from ergonomica.tokenizer import tokenize



def echo(string):
    """Example function that prints its input."""
    print(string)

def while(args):
    while namespace[args[0]]:
        namespace[args[1]](args[2:])
    
namespace = {'echo': echo}


operations = []

class Function(object):
    name = False
    body = False
    
    def __init__(self):
        pass

lines = "\n" + open(sys.argv[1], "r").read()

tokens = tokenize(lines)

def make_function(string):
    def f(x):
        return eval_tokens(string)
    return f

def ergo(stdin):
    return eval_tokens(tokenize(stdin))

def eval_tokens(tokens):
    
    new_command = True
    in_function = False

    f = False
    args = []
    skip = True
    depth = 0
    
    for token in tokens:

        if token.type == "END":
            depth -= 1
            if depth == 0:
                in_function = False
                function.body.append(tokenize("\n")[0])
                namespace[function.name] = make_function(function.body)
                continue

        if in_function:
            if token.type == 'DEFINITION':
                depth += 1
            elif (not function.name):
                function.name = token.value
                continue
            function.body.append(token)
            continue
                    
        # recognize commands as distinct from arguments
        if (token.type == 'NEWLINE') or (token.type == 'PIPE'):
            if f:
                f = namespace[f]
                f(args)
                f = False
                args = []
                
            new_command = True
            skip = True

            if in_function:
                function.body.append(token)
            continue

        elif skip:
            skip = False

        else:
            new_command = False

        if token.type == 'DEFINITION':
            in_function = True
            function = Function()
            function.body = []
            depth += 1
            continue
    
        elif (not new_command) and in_function:
            if not function.name:
                function.name = token.value
                pass
            else:
                function.body.append(token)
        
        if new_command and in_function:
            function.body.append(token)
            
        
        elif new_command and (not in_function):
            if not f:
                f = token.value
            else:
                f = namespace[token.value]
                f(args)
                f = False
                args = []
                
        elif (not new_command) and (not in_function):
            args.append(token.value)

eval_tokens(tokens)

