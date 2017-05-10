#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[ergo.py]

The main Ergonomica runtime.
"""

from __future__ import absolute_import, print_function

#import sys
import argparse
from ergonomica.tokenizer import tokenize
from docopt import docopt

#
# ergonomica library imports
#

#from lib.lang.environment import Environment
from ergonomica.lib.interface.prompt import prompt
#from lib.lang.arguments import get_args_kwargs, get_func

# import all commands
from ergonomica.lib.load_commands import verbs
from ergonomica.lib.lang.environment import Environment

# initialize environment variable
# TODO: load config file
ENV = Environment()

def t(args):
    return True

def f(args):
    return False

ENV.verbs.update(verbs)

# variables
VNAMESPACE = {}

class Function(object):
    name = False
    body = False
    
    def __init__(self):
        pass

def make_function(tokens):
    """Make a function that evaluates ergonomica on the tokens specified at runtime."""
    def f(x):
        """An Ergonomica runtime function."""
        return eval_tokens(tokens)
    return f

def ergo(stdin):
    return eval_tokens(tokenize(stdin + "\n"))

def eval_tokens(tokens, log=False):#substitutions, log=False):
    
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
                ENV.verbs[function.name] = make_function(function.body)
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
                f = ENV.verbs[f]
                eval_f = f(ENV, docopt("usage: function " + f.__doc__.split("@")[0], argv=args))
                if eval_f:
                    if isinstance(eval_f, list):
                        map(print, eval_f)
                    else:
                        print(eval_f)
                        
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
            else:
                function.body.append(token)
        
        if new_command and in_function:
            function.body.append(token)
            
        
        elif new_command and (not in_function):
            if not f:
                f = token.value
            else:
                f = ENV.verbs[token.value]
                eval_f = f(ENV, docopt("usage: function " + f.__doc__.split("@")[0], argv=args))
                if eval_f:
                    if isinstance(eval_f, list):
                        map(print, eval_f)
                    else:
                        print(eval_f)
                        
                f = False
                args = []
                
        elif (not new_command) and (not in_function):
            if token.type == 'SUBSTITUTION':
                pass
                #args.append(substitutions[int(token.value[1:])])
            else:
                args.append(token.value)

#
# set up argparse
#

ARGPARSER = argparse.ArgumentParser(description='The Ergonomica shell.')
ARGPARSER.add_argument('-f', '--file', help='Run an ergonomica file.', nargs='?')
ARGPARSER.add_argument('-log', help='Show ergonomica debug messages')

args = ARGPARSER.parse_args()

#if args.file and args.log:

if args.file:
    ergo(open(args.file, 'r').read())

else:
    while True:
        stdin = prompt()
        ergo(stdin)
