#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The Ergonomica interpreter.

Usage:
  ergo.py [--file <file>] [--log]
  ergo.py [--login] [--log]
  ergo.py -h | --help
  ergo.py --version

Options:
  -h --help      Show this screen.
  --version      Show version.
  --file <file>  Specify an Ergonomica script to run.
  --log          Show debugging log.
"""

from __future__ import absolute_import, print_function

import os
from docopt import docopt

#
# ergonomica library imports
#

from ergonomica.lib.interface.prompt import prompt
from ergonomica.lib.lang.namespace import Namespace
from ergonomica.lib.load_commands import verbs
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.pipe import Pipeline, Operation
from ergonomica.tokenizer import tokenize


# initialize environment variable
ENV = Environment()

def t(args):
    return True

def f(args):
    return False

ENV.verbs.update(verbs)

ns=ENV.verbs
ns["t"] = t
ns["f"] = f

class Function(object):
    name = False
    body = False
    argspec = ""
    
    def __init__(self):
        pass

def make_function(ns, function):
    def f(argc):
        """An Ergonomica runtime function."""
        ns = argc.ns
        for item in argc.args:
            ns[unicode(item)] = argc.args[item]
        return eval_tokens(function.body, ns)#, Pipeline(argc.env, ns))
    try:
        f.__doc__ = function.argspec[1:] + "@"
    except IndexError:
        f.__doc__ = "@"
    return f

def ergo(stdin, log=False):
    return eval_tokens(tokenize(stdin + "\n"), ENV.verbs, log=log)

def eval_tokens(tokens, ns, log=False, silent=False):

    global pipe
    
    new_command = True
    in_function = False
    
    argspec = False
    
    function = Function()
    
    f = False
    args = []
    skip = False
    depth = 0
    doc = []
    
    pipe = Pipeline(ENV, ns)
    pipe.operations = []
    pipe.args =  []
    
    for token in tokens:

        if log:
            print("--- [ERGONOMICA LOG] ---")
            print("CURRENT TOKEN: ", token)
            print("CURRENT args : ", args)
            print("F is         : ", f)
            print("NEW_COMMAND  : ", new_command)
            print("------------------------\n")
            
        # recognize commands as distinct from arguments
        if (token.type == 'NEWLINE'):
            
            argspec = False
         
            if in_function:
                function.body.append(token)
                continue

            if f:
                pipe.append_operation(Operation(f, args))
                stdout = pipe.STDOUT()
                if (stdout != None) and (not silent):
                    if isinstance(stdout, list):
                        for item in stdout:
                            if item:
                                print(item)
                    else:
                        print(stdout)
                pipe = Pipeline(ENV, ns) 

            if skip:
                skip = False
                continue

            new_command = True
            continue
                            
        if token.type == 'PIPE':
            #try:
            pipe.append_operation(Operation(f, args))
            #except KeyError:
            #    print("[ergo: CommandError]: Unknown command '%s'." % f)
                
            f = False
            args = []
            new_command = True
            continue
        
        if token.type == "END":
            depth -= 1
            if depth == 0:
                in_function = False
                ns[unicode(function.name)] = make_function(ns, function)
                skip = True
                continue
        
        if in_function:
            if token.type == 'DEFINITION':
                depth += 1
                skip = True
                function.body.append(token)
                continue

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
                #try:
                f = ns[token.value]
                    #doc = f.__doc__.split("@")[0]
                #except KeyError:
                #    print("[ergo: CommandError]: No such command '%s'." % (token.value))
                    
                new_command = False
                continue
                
        elif (not new_command) and (not in_function):
            args.append(token.value)

def main():
    arguments = docopt(__doc__)

    ns = ENV.verbs
    
    # help already covered by docopt
    if arguments['--version']:
        print('[ergo]: Version 2.0.0-alpha.1')

    else:
        log = arguments['--log']

        if arguments['--file']:
            ergo(open(arguments['--file'], 'r').read(), log=log)

        else:
            ns = ENV.verbs # persistent namespace across all REPL loops
            if arguments['--login']:
                eval_tokens(tokenize(open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")).read() + "\n"), ns, log=log, silent=True)

            while ENV.run:
                stdin = prompt(ENV, ns)
                eval_tokens(tokenize(stdin + "\n"), ns, log=log)

            
if __name__ == '__main__':
    main()
