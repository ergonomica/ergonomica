#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[ergo.py]

The main Ergonomica runtime.
"""

from __future__ import absolute_import

import sys
from tokenizer import tokenize

#
# ergonomica library imports
#

#from lib.lang.environment import Environment
from lib.interface.prompt import prompt
from ergonomica.lib.lang.arguments import get_args_kwargs, get_func

# import all commands
from ergonomica.lib.load.load_commands import verbs


# initialize environment variable
# TODO: load config file
#ENV = Environment()


def echo(string):
    """ARG,...@Example function that prints its input."""
    print(string)

def e_while(args):
    """Ergonomica while loop implementation."""
    while FNAMESPACE[args[0]]:
        FNAMESPACE[args[1]](args[2:])

def e_if(args):
    """Ergonomica if conditional implementation"""
    if FNAMESPACE[args[0]]:
        FNAMSPACE[args[1]](args[2:])

def t(args):
    return True

def f(args):
    return False

# functions
FNAMESPACE = {'echo': echo,
             'while': e_while,
             'if': e_if,
             't': t, 'f':f}

# variables
VNAMESPACE = {}

class Function(object):
    name = False
    body = False
    
    def __init__(self):
        pass

#class Pipeline(object):

#    def __init__(self):
#        self.function = lambda x: x
#        pass

#    def append_func(self, f)

def make_function(tokens):
    """Make a function that evaluates ergonomica on the tokens specified at runtime."""
    def f(x):
        """An Ergonomica runtime function."""
        return eval_tokens(tokens)
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
                FNAMESPACE[function.name] = make_function(function.body)
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
                f = FNAMESPACE[f]
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
                f = FNAMESPACE[token.value]
                f(args)
                f = False
                args = []
                
        elif (not new_command) and (not in_function):
            args.append(token.value)

# REPL loop
while True:
    stdin = prompt()
    ergo(stdin)

