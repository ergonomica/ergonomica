#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The Ergonomica interpreter.

Usage:
  ergo.py [--file <file>] [--log]
  ergo.py -h | --help
  ergo.py --version

Options:
  -h --help      Show this screen.
  --version      Show version.
  --file <file>  Specify an Ergonomica script to run.
  --log          Show debugging log.
"""

from __future__ import absolute_import, print_function

from docopt import docopt

#
# ergonomica library imports
#

from ergonomica.lib.interface.prompt import prompt
from ergonomica.lib.lang.namespace import Namespace
from ergonomica.lib.load_commands import verbs
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.pipe import Pipeline, Operation
from ergonomica.lib.lang.arguments import ArgumentsContainer
from ergonomica.tokenizer import tokenize

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
    def f(argc):
        """An Ergonomica runtime function."""
        ns = argc.ns
        for item in argc.args:
            ns[unicode(item)] = argc.args[item]
        return eval_tokens(function.body, ns)
    f.__doc__ = function.argspec[1:] + "@"
    return f

def ergo(stdin, log=False):
    return eval_tokens(tokenize(stdin + "\n"), ENV.verbs, log=log)

def eval_tokens(tokens, ns, log=False):
    
    new_command = True
    in_function = False

    pipe = Pipeline(ENV, ns)
    
    function = Function()
    
    f = False
    args = []
    skip = True
    depth = 0
    
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
            if f:
                pipe.append_operation(Operation(ns[f], args))
            if pipe.operations:
                try:
                    f = ns[unicode(f)]
                except KeyError:
                    print("[ergo: CommandError]: Unknown command '%s'." % f)
                    return

                stdout = pipe.STDOUT()    
                if stdout:
                    if isinstance(stdout, list):
                        map(print, stdout)
                    else:
                        print(stdout)
                        
                f = False
                args = []
                
            new_command = True
            skip = True

            if in_function:
                function.body.append(token)
            continue

                            
        #elif skip:
        #    skip = False

        #else:
        #    new_command = False

        
        if token.type == 'PIPE':
            try:
                pipe.append_operation(Operation(ns[f], args))
            except KeyError:
                print("[ergo: CommandError]: Unknown command '%s'." % f)
                
            f = False
            args = []
            new_command = True
            continue

        
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
                new_command = False
                continue
                
        # elif new_command and (not in_function):
        #     if not f:
        #         f = token.value
        #     else:
        #         try:
        #             f = ns[unicode(f)]
        #         except KeyError:
        #             print("[ergo: CommandError]: Unknown command '%s'." % f)
        #             return
                
        #         eval_f = f(ENV, ns, docopt("usage: function " + f.__doc__.split("@")[0], argv=args))
        #         if eval_f:
        #             if isinstance(eval_f, list):
        #                 map(print, eval_f)
        #             else:
        #                 print(eval_f)
                        
        #         f = False
        #         args = []
                
        elif (not new_command) and (not in_function):
            #if token.type == 'SUBSTITUTION':
            #    pass
            #    #args.append(substitutions[int(token.value[1:])])
            args.append(token.value)

if __name__ == '__main__':
    arguments = docopt(__doc__)

    # help already covered by docopt
    if arguments['--version']:
        print('[ergo]: Version 2.0.0-alpha.1')

    else:
        log = arguments['--log']

        if arguments['--file']:
            ergo(open(arguments['--file'], 'r').read(), log=log)

        else:
            ns = ENV.verbs # persistent namespace across all REPL loops
            while True:
                stdin = prompt(ENV, ns)
                eval_tokens(tokenize(stdin + "\n"), ns, log=log)
