#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The Ergonomica interpreter.

Usage:
  ergo.py [-files FILE...] [--log]
  ergo.py [--login] [--log]
  ergo.py -h | --help
  ergo.py --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  --files FILE... Specify an Ergonomica script to run.
  --log           Show debugging log.
"""

from __future__ import absolute_import, print_function

import os
from docopt import docopt
import uuid
import traceback
import sys

#
# ergonomica library imports
#

from ergonomica.lib.interface.prompt import prompt
from ergonomica.lib.lang.namespace import Namespace
from ergonomica.lib.load_commands import verbs
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.pipe import Pipeline, Operation
from ergonomica.lib.lang.tokenizer import tokenize

# initialize environment variable
ENV = Environment()

PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")

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

def eval_tokens(*args, **kwargs):
    return list(raw_eval_tokens(*args, **kwargs))
    
def make_function(ns, function):
    def f(argc):
        """An Ergonomica runtime function."""
        ns = argc.ns
        for item in argc.args:
            ns[unicode(item)] = argc.args[item]
        return eval_tokens(function.body, ns)

    f.__doc__ = function.argspec[1:]
    if f.__doc__ == "":
        f.__doc__ = "usage: function"
    return f

def ergo(stdin, log=False):
    return eval_tokens(tokenize(stdin + "\n"), ENV.verbs, log=log)

lambda_dict = {}

def raw_eval_tokens(_tokens, ns, log=False, silent=False):

    global pipe
    
    new_command = True
    in_function = False
    in_lambda = False
    argspec = False

    function = Function()
    f = False
    args = []
    skip = False
    depth = 0
    lambda_depth = 0
    _lambda = []
    doc = []
    eval_next_expression = False
    current_indent = 0
    
    pipe = Pipeline(ENV, ns)
    pipe.operations = []
    pipe.args =  []

    tokens = _tokens
    
    tokens.append(tokenize("\n")[0])
    tokens[-1].type = 'EOF'

    for i in range(len(tokens)):

        token = tokens[i]
                
        if log:
            print("--- [ERGONOMICA LOG] ---")
            print("CURRENT TOKEN: ", token)
            print("CURRENT args : ", args)
            print("F is         : ", f)
            print("NEW_COMMAND  : ", new_command)
            print("------------------------\n")
    
        if not in_function:
            if token.type == 'EVAL':
                eval_next_expression = True
    
            if token.type == 'LBRACKET':
                lambda_depth += 1
                in_lambda = True

            if in_lambda:
                if token.type == 'RBRACKET':
                    lambda_depth -= 1
                    
                if lambda_depth != 0:
                    _lambda.append(token)
                    continue
                    
                else: # time to wrap up the function
                    token.type = 'LITERAL'
                    del _lambda[0]
                    _lambda.append(tokenize("\n")[0])

                    if eval_next_expression:
                        token.value = eval_tokens(_lambda, ns, log=log, silent=silent)
                        eval_next_expression = False
                    else:
                        u = str(uuid.uuid1())
                        ns[u] = lambda x: eval_tokens(_lambda, ns, log=log, silent=silent)
                        token.value = u
                        
                    in_lambda = False
                    
        if in_lambda and not in_function:           
            if token.type == 'RBRACKET':
                lambda_depth -= 1


        if (token.type == 'EOF')  or ((token.type == 'NEWLINE') and (tokens[i+1].type != 'INDENT')):
            if in_function:
                in_function = False
                function.body.append(tokenize("\n")[0])
                print(function.body)
                ns[unicode(function.name)] = make_function(ns, function)
                #skip = True
            else:
                token.type == 'NEWLINE'
                
        # recognize commands as distinct from arguments
        if (token.type == 'NEWLINE'):
            
            argspec = False
            current_indent = 0
            skip = False
            
            if tokens[i+1].type == 'INDENT':
                function.body.append(token)
                continue
            
            if in_function:
                function.body.append(token)
                continue

            if f:
                pipe.append_operation(Operation(f, args))
                stdout = pipe.STDOUT()
                if (stdout != None) and (not silent):
                    if isinstance(stdout, list):
                        for item in stdout:
                            yield item
                    else:
                        yield stdout
                pipe = Pipeline(ENV, ns) 

            if skip:
                skip = False
                continue

            new_command = True
            continue
                            
        if token.type == 'PIPE':
            try:
                pipe.append_operation(Operation(f, args))
            except KeyError:
                print("[ergo: CommandError]: Unknown command '%s'." % f)
                
            f = False
            args = []
            new_command = True
            continue

        if token.type == "INDENT":
            if not current_indent:
                current_indent += 1
                continue
            current_indent += 1

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
                try:
                    f = ns[token.value]
                except KeyError:
                    if len(token.value) == 3:
                        possible_matches = [x for x in ns if x.startswith(token.value)]
                        if len(possible_matches) == 1:
                            f = ns[token.value]
                    #print("[ergo: CommandError]: Unknown command '%s'." % (token.value))
                    f = token.value
                    
                new_command = False
                continue
                
        elif (not new_command) and (not in_function):
            args.append(token.value)

def main():
    # parse arguments through Docopt
    arguments = docopt(__doc__)

    # help already covered by docopt
    if arguments['--version']:
        print('[ergo]: Version 2.0.0')

    else:
        # whether we want devlog or not
        log = arguments['--log']
        
        if '--file' in arguments and arguments['--file']:
            ergo(open(arguments['--file'], 'r').read(), log=log)

        else:
            # persistent namespace across all REPL loops
            ns = ENV.verbs
    
            
            # if run as login shell, run .ergo_profile
            if arguments['--login']:
                eval_tokens(tokenize(open(PROFILE_PATH).read() + "\n"), ns, log=log, silent=True)

            # REPL loop
            while ENV.run:
                try:
                    stdin = prompt(ENV, ns)
                    try:
                        stdout = eval_tokens(tokenize(stdin + "\n"), ns, log=log)
                    except Exception:
                        traceback.print_exc(file=sys.stdout)
                        continue
                    
                    for i in stdout:
                        if i != '':
                            print(i)
                    
                # allow for interrupting functions. Ergonomica can still be suspended from within Bash with C-z.
                except KeyboardInterrupt:
                    print("[ergo: KeyboardInterrupt]: Exited.")
                    
            
if __name__ == '__main__':
    main()
