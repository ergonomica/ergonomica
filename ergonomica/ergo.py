 #!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The Ergonomica interpreter.

Usage:
  ergo.py [--file FILE] [--log] [--login]
  ergo.py [-m STRING] [--log] [--login]
  ergo.py -h | --help
  ergo.py --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  --files FILE... Specify an Ergonomica script to run.
  --log           Show debugging log.
"""

from __future__ import absolute_import, print_function

import inspect
import os
import uuid
import traceback
import sys
from copy import copy
import threading
import subprocess

# for escaping shell commands
try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote

from ergonomica.lib.lang.tokenizer import tokenize
from ergonomica.lib.lang.docopt import docopt, DocoptException

#
# ergonomica library imports
#

from ergonomica.lib.interface.prompt import prompt
from ergonomica.lib.lib import ns
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.arguments import ArgumentsContainer
from ergonomica.lib.lang.builtins import Namespace, namespace

# initialize environment variables
ENV = Environment()
PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")

# for handling double-printing with shell commands that output to STDOUT
PRINT_OUTPUT = True

def validate_symbol(symbol):
    """
    Throws appropriate exceptions on an invalid symbol.
    """

    if "]" in symbol:
        if not symbol.endswith("]"):
            raise SyntaxError("[ergo: SyntaxError]: Unexpected \"]\" in Symbol \"{}\".".format(symbol))
        else:
            try:
                int(symbol[(symbol.find("[") + 1):symbol.find("]")])
            except ValueError:
                raise SyntaxError("[ergo: SyntaxError]: Non-integer index specified in Symbol \"{}\".".format(symbol))
                              
    elif "[" in symbol:
        raise SyntaxError("[ergo: SyntaxError]: Unexpected \"[\" in Symbol \"{}\".".format(symbol))

class Symbol(str):
    def __init__(self, value):
        super().__init__()
        validate_symbol(value)

class Function(object):
    def __init__(self, args, body, ns):
        self.args = args
        self.body = body
        self.ns = ns

    def __call__(self, *args):
        out = [eval(sexp, Namespace(self.args, args, self.ns)) for sexp in self.body]
        if len(out) == 1:
            return out[0]
        else:
            return [x for x in out if x != None]

namespace.update(ns)

def ergo(stdin):
    """Wrapper for Ergonomica tokenizer and evaluator."""
    try:
        return eval(parse(tokenize(stdin)), namespace)
    except Exception as e:
        print(e)
    
def unquote(str):
    """Remove quotes from a string."""
    if len(str) > 1:
        if str.startswith('"') and str.endswith('"'):
            return str[1:-1].replace('\\\\', '\\').replace('\\"', '"')
        if str.startswith('<') and str.endswith('>'):
            return str[1:-1]
    return str


def parse(tokens):
    depth = 0
    L = []
    parsed_command = False # switch set to true on first atom parsed---ensures that
                           # arguments after the command interpreted as strings
    parsed_tokens = []
    for token in tokens:
        if depth > 0:
            if token == ")":
                depth -= 1
            elif token == "(":
                depth += 1
            if depth == 0:
                parsed_tokens.append(parse(L))
                L = []
            else:
                L.append(token)
            continue
                
        if token == "(":
            depth = 1
            continue

        if token == "|":
            parsed_command = False
            parsed_tokens.append(token)
            continue
        
        if not parsed_command or token.startswith("#"):
            parsed_tokens.append(Symbol(token))
            parsed_command = True
            
        else:
            try:
                parsed_tokens.append(int(token))
            except ValueError: 
                try: 
                    parsed_tokens.append(float(token))
                except ValueError:
                    # it's a string or Symbol
                    if token.startswith("$"):
                        parsed_tokens.append(Symbol(token[1:])) # make a Symbol with the $ stripped away
                    else:
                        if token.startswith("'") or token.startswith("\""):
                            parsed_tokens.append(unquote(token))
                        else:
                            parsed_tokens.append(token)

    return parsed_tokens


def check_token(token):
    """Raise a SyntaxError on a malformed token."""
    if (token.startswith("'") and token.endswith("'")) or \
       (token.startswith("\"") and token.endswith("\"")):
        return

def atom(token, no_symbol=False):
    try:
        return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            if token.startswith("'") or token.startswith("\""):
                return token[1:-1]
            elif no_symbol:
                print(token)
                if token.startswith("#"):
                    return Symbol(token)
                else:
                    return token
            else:
                return Symbol(token)

def eval(x, ns):
    global namespace, PRINT_OUTPUT
    
    PRINT_OUTPUT = True
    if isinstance(x, Symbol):
        try:
            if ("[" in x) and x.endswith("]"):
                index = x[x.find("[") + 1:x.find("]")]
                return ns.find(x[:x.find("[")])[x[:x.find("[")]].__getitem__(atom(index, no_symbol=True))
            else:
                return ns.find(x)[x]
        except AttributeError as error:
            raise NameError("[ergo]: NameError: No such variable {}.".format(x))

    elif isinstance(x, str):
        return x

    elif not isinstance(x, list):
        return x
    
    elif x[0] == "if":
        if len(x) == 4:
            (_, conditional, then, _else) = x
            exp = (then if eval(conditional, ns) else _else)
        elif len(x) == 3:
            (_, conditional, then) = x
            exp = (then if eval(conditional, ns) else None)
        else:
            raise SyntaxError("[ergo: SyntaxError]: Wrong number of arguments for `if`. Should be: if conditional then [else].")
        return eval(exp, ns)
    
    elif x[0] == "set":
        if len(x) == 3:
            (_, name, body) = x
            name = Symbol(name)
            ns[name] = eval(body, ns)
        else:
            raise SyntaxError("[ergo: SyntaxError]: Wrong number of arguments for `set`. Should be: set symbol value.")
    
    elif x[0] == "global":
        (_, name, body) = x
        name = Symbol(name)
        namespace[name] = eval(body, ns)

    elif x[0] == "lambda":
        if len(x) > 2:
            argspec = x[1]
            body = x[2:]
            return Function(argspec, body, ns)
        else:
            print(x)
            raise SyntaxError("[ergo: SyntaxError]: Wrong number of arguments for `lambda`. Should be: lambda argspec body....")

        
    else:
        try:
            if inspect.getfullargspec(eval(x[0], ns)).args == ['argc']:
                return eval(x[0], ns)(ArgumentsContainer(ENV, namespace, docopt(eval(x[0], ns).__doc__, [eval(i, ns) for i in x[1:]])))
            return eval(x[0], ns)(*[eval(i, ns) for i in x[1:]])
        except NameError as e:
            if not e.args[0].startswith("[ergo]: NameError: No such variable"):
                # then it's not actually a unknown command---it's an error from something else
                raise e
            # presumably the command isn't found
            try:
                p = subprocess.Popen([x[0]] + [eval(i, ns) for i in x[1:]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                cur = []
                for line in iter(p.stdout.readline, ""):
                    print(line)
                    cur.append(line)
                PRINT_OUTPUT = False
                return cur
                
            except FileNotFoundError:
                return ("[ergo]: Unknown command '{}'.".format(x[0]))
            

def main():
    """The main Ergonomica runtime."""

    global PRINT_OUTPUT
    
    # parse arguments through Docopt
    arguments = docopt(__doc__)

    # persistent namespace across all REPL loops
    # namespace = ENV.ns


    # help already covered by docopt
    if arguments['--version']:
        print('[ergo]: Version 2.0.0')

    else:
        # whether we want devlog or not
        log = arguments['--log']

        if '--file' in arguments and arguments['--file']:
            stdout = eval_tokens(tokenize(open(arguments['FILE']).read() + "\n"), namespace, log=log)

        elif arguments['-m']:
            print(ergo(arguments['STRING'], log=log))

        else:

            # if run as login shell, run .ergo_profile
            if arguments['--login']:
                pass

            # REPL loop
            while ENV.run:
                try:
                    stdin = str(prompt(ENV, copy(namespace)))
                    
                    stdout = ergo(stdin)

                    if PRINT_OUTPUT:
                        if isinstance(stdout, list):
                            print("\n".join([str(x) for x in stdout]))
                        else:
                            if stdout != None:
                                print(stdout)

                # allow for interrupting functions. Ergonomica can still be
                # suspended from within Bash with C-z.
                except KeyboardInterrupt:
                    print("[ergo: KeyboardInterrupt]: Exited.")


if __name__ == '__main__':
    main()


    
