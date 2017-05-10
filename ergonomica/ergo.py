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
from ergonomica.lib.lang.namespace import Namespace

# import all commands
from ergonomica.lib.load_commands import verbs
from ergonomica.lib.lang.environment import Environment

# initialize environment variable
# TODO: load config file
ENV = Environment()
ns = Namespace()

def t(args):
    return True

def f(args):
    return False

ENV.verbs.update(verbs)

class Function(object):
    name = False
    body = False
    argspec = ""
    
    def __init__(self):
        pass

def make_function(ns, function):
    def f(env, namespace, args):
        """An Ergonomica runtime function."""
        ns = namespace
        for item in args:
            ns[unicode(item)] = args[item]
        return eval_tokens(function.body, ns)
    f.__doc__ = function.argspec[1:] + "@"
    return f

def ergo(stdin):
    return eval_tokens(tokenize(stdin + "\n"), ENV.verbs)

def eval_tokens(tokens, ns, log=False):
    
    new_command = True
    in_function = False

    function = Function()
    
    f = False
    args = []
    skip = True
    depth = 0
    
    for token in tokens:

        # recognize commands as distinct from arguments
        if (token.type == 'NEWLINE') or (token.type == 'PIPE'):
            argspec = False
            if f:
                try:
                    f = ns[unicode(f)]
                except KeyError:
                    print("[ergo: CommandError]: Unknown command '%s'." % f)
                    return
                    
                eval_f = f(ENV, ns, docopt("usage: function " + f.__doc__.split("@")[0], argv=args))
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

        
        if token.type == "END":
            depth -= 1
            if depth == 0:
                in_function = False
                function.body.append(tokenize("\n")[0])
                ns[unicode(function.name)] = make_function(ns, function)
                continue
        
        if in_function:
            if token.type == 'DEFINITION':
                depth += 1
                continue
            if token.type == 'NEWLINE':
                argspec = False
            elif (not function.name):
                function.name = token.value
                argspec = True
                continue
            elif argspec:
                function.argspec += " " + token.value
                continue

            function.body.append(token)
            continue
        
        if token.type == 'VARIABLE':
            token.type = 'LITERAL'
            token.value = str(ns[unicode(token.value)])

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
                try:
                    f = ns[unicode(f)]
                except KeyError:
                    print("[ergo: CommandError]: Unknown command '%s'." % f)
                    return
                
                eval_f = f(ENV, ns, docopt("usage: function " + f.__doc__.split("@")[0], argv=args))
                if eval_f:
                    if isinstance(eval_f, list):
                        map(print, eval_f)
                    else:
                        print(eval_f)
                        
                f = False
                args = []
                
        elif (not new_command) and (not in_function):
            #if token.type == 'SUBSTITUTION':
            #    pass
            #    #args.append(substitutions[int(token.value[1:])])
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
    ns = ENV.verbs
    while True:
        stdin = prompt()
        eval_tokens(tokenize(stdin + "\n"), ns)
