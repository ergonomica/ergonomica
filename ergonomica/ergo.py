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
import types

# for escaping shell commands
try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote

# Python2 doesn't have FileNotFoundError
try:
    FileNotFoundError
except NameError:
    # define a new FileNotFoundError. Since this is Py2,
    # it won't be thrown, and it will default to whatever else
    # is thrown
    class FileNotFoundError(IOError):
        pass

from ergonomica import ErgonomicaError
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
from ergonomica.lib.lang.parser import Symbol, parse

# initialize environment variables
ENV = Environment()
PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")


# Override printing. This is done because
# the output of shell commands is printed procedurally,
# and you don't want the same output printed twice.
PRINT_OVERRIDE = False

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
    if stdin.strip() == "":
        return None
    try:
        return eval(parse(tokenize(stdin)), namespace, True)
    except Exception as e:
        if isinstance(e, ErgonomicaError) or isinstance(e, DocoptException) or isinstance(e, KeyboardInterrupt):
            print(e)
        else:
            traceback.print_exc()

def print_ergo(stdin):
    """Wrapper for Ergonomica tokenizer and evaluator."""
    global PRINT_OVERRIDE
    
    stdout = ergo(stdin)
    
    if not PRINT_OVERRIDE:
        if isinstance(stdout, list):
            print("\n".join([str(x) for x in stdout]))
        else:
            if stdout != None:
                print(stdout)
    
def file_lines(stdin):
    split_lines = []
    for line in stdin.split("\n"):
        if line.startswith(" "):
            split_lines[-1] += line
        else:
            split_lines.append(line)
    return split_lines
        

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

def arglist(function):
    if isinstance(function, types.FunctionType):
        return inspect.getargspec(function).args
    else:
        return inspect.getargspec(function.__call__).args
        
    
def eval(x, ns, at_top = False):
    global namespace, PRINT_OVERRIDE

    if at_top:
        PRINT_OVERRIDE = False
    
    if x == []:
        return
    
    if isinstance(x, Symbol):
        try:
            if ("[" in x) and x.endswith("]"):
                index = x[x.find("[") + 1:x.find("]")]
                return ns.find(x[:x.find("[")])[x[:x.find("[")]].__getitem__(atom(index, no_symbol=True))
            else:
                return ns.find(x)[x]
        except AttributeError as error:
            raise ErgonomicaError("[ergo]: NameError: No such variable {}.".format(x))

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
            raise ErgonomicaError("[ergo: SyntaxError]: Wrong number of arguments for `if`. Should be: if conditional then [else].")
        return eval(exp, ns)
    
    elif x[0] == "set":
        if len(x) == 3:
            (_, name, body) = x
            name = Symbol(name)
            ns[name] = eval(body, ns)
        else:
            raise ErgonomicaError("[ergo: SyntaxError]: Wrong number of arguments for `set`. Should be: set symbol value.")
    
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
            raise ErgonomicaError("[ergo: SyntaxError]: Wrong number of arguments for `lambda`. Should be: lambda argspec body....")

        
    else:
        try:
            if arglist(eval(x[0], ns)) == ['argc']:
                return eval(x[0], ns)(ArgumentsContainer(ENV, namespace, docopt(eval(x[0], ns).__doc__, [eval(i, ns) for i in x[1:]])))
            return eval(x[0], ns)(*[eval(i, ns) for i in x[1:]])
        except ErgonomicaError as e:
            if not e.args[0].startswith("[ergo]: NameError: No such variable"):
                # then it's not actually a unknown command---it's an error from something else
                raise e
            # presumably the command isn't found
            try:
                if x[0].startswith("%"):
                    return os.system(" ".join([x[0][1:]] + [eval(i, ns) for i in x[1:]]))
                else:
                    if at_top:
                        PRINT_OVERRIDE = True
                    
                    p = subprocess.Popen([x[0]] + [str(eval(i, ns)) for i in x[1:]], stdout=subprocess.PIPE, universal_newlines=True)
                    cur = []
                    try:
                        for line in iter(p.stdout.readline, ""):
                            line = line[:-1] # remove the trailing newline
                            if at_top:
                                print(line)
                            cur.append(line)
                    except KeyboardInterrupt as e:
                        p.terminate()
                        raise e
                            
                    if len(cur) == 1:
                        return cur[0]
                    else:
                        return cur
                    
            except FileNotFoundError:
                raise ErgonomicaError("[ergo]: Unknown command '{}'.".format(x[0]))
            
            except OSError: # on Python2
                raise ErgonomicaError("[ergo]: Unknown command '{}'.".format(x[0]))
            

def main():
    """The main Ergonomica runtime."""

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
            for line in file_lines(open(arguments['FILE']).read()):
               print_ergo(line)
    
            
        elif arguments['-m']:
            print_ergo(arguments['STRING'])

        else:

            # if run as login shell, run .ergo_profile
            if arguments['--login']:
                for line in file_lines(open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")).read()):
                    print_ergo(line)
                
            # REPL loop
            while ENV.run:
                try:
                    stdin = str(prompt(ENV, copy(namespace)))

                    print_ergo(stdin)


                # allow for interrupting functions. Ergonomica can still be
                # suspended from within Bash with C-z.
                except KeyboardInterrupt:
                    print("[ergo: KeyboardInterrupt]: Exited.")


if __name__ == '__main__':
    main()
