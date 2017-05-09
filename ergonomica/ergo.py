#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[ergo.py]

The main Ergonomica runtime.
"""

from __future__ import absolute_import, print_function

#import sys
import argparse
from tokenizer import tokenize

#
# ergonomica library imports
#

#from lib.lang.environment import Environment
from lib.interface.prompt import prompt
#from lib.lang.arguments import get_args_kwargs, get_func

# import all commands
from lib.load_commands import verbs
from lib.lang.environment import Environment

# initialize environment variable
# TODO: load config file
ENV = Environment()

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

FNAMESPACE.update(verbs)

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
    return eval_tokens(tokenize(stdin + "\n"))

def eval_tokens(tokens, log=False):
    
    new_command = True
    in_function = False

    function = Function()
    
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
                
                eval_f = f(ENV, args)
                if eval_f:
                    map(print, eval_f)
                
                
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
                eval_f = f(ENV, args)
                if eval_f:
                    map(print, eval_f)

                f = False
                args = []
                
        elif (not new_command) and (not in_function):
            args.append(token.value)


#
# set up argparse
#

argparser = argparse.ArgumentParser(description='The Ergonomica shell.')
argparser.add_argument('-f', '--file', help='Run an ergonomica file.', nargs='?', default='haha')
argparser.add_argument('-log', help='Show ergonomica debug messages')

args = argparser.parse_args()

#if args.file and args.log:

if args.file:
    ergo(open(args.file, 'r').read())

else:
    while True:
        stdin = prompt()
        ergo(stdin)
