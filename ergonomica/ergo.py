#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The Ergonomica interpreter.

Usage:
  ergo.py [--login]
  ergo.py [--login] FILE [FILE_ARGV...]
  ergo.py [--login] [(-s | --string) STRING]

Options:
  --login         Source ~/.ergo/.ergo_profile on startup.
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

class function(object):
    def __init__(self, args, body, ns):
        self.args = args
        self.body = body
        self.ns = ns

    def __call__(self, *args):
        return eval(self.body, Namespace(self.args, args, self.ns))

namespace.update(ns)

def source(filename):
    for line in file_lines(open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")).read()):
        print_ergo(line)

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

def expand_typed_args(args):
    return [(" ".join([str(y) for y in x]) if isinstance(x, list) else str(x)) for x in args]
            
def print_ergo(stdin):
    """Wrapper for Ergonomica tokenizer and evaluator."""
    global PRINT_OVERRIDE
    
    stdout = ergo(stdin)
    
    if not PRINT_OVERRIDE:
        if isinstance(stdout, list):
            print("\n".join([str(x) for x in stdout if x != None]))
        else:
            if stdout != None:
                print(stdout)
    
def file_lines(stdin):
    split_lines = []
    for line in stdin.split("\n"):
        if line.startswith("#"):
            pass
        elif line.startswith(" "):
            split_lines[-1] += line
        else:
            split_lines.append(line)
    return split_lines
        

namespace['source'] = lambda filename: [ergo(line) for line in file_lines(open(filename).read())]

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
    # they don't have args attributes since they're not actual Python functions
    if isinstance(function, types.BuiltinFunctionType):
        return []
    elif isinstance(function, types.FunctionType):
        return inspect.getargspec(function).args
    else:
        return inspect.getargspec(function.__call__).args
        
    
def eval(x, ns, at_top = False):
    global namespace, PRINT_OVERRIDE, ENV

    if at_top:
        PRINT_OVERRIDE = False

    while True:
        if x == []:
            return
        
        if isinstance(x, Symbol):
            try:
                return ns.find(x)[x]
            except AttributeError as error:
                raise ErgonomicaError("[ergo]: NameError: No such variable {}.".format(x))
        
        elif isinstance(x, str):
            return x
        
        elif not isinstance(x, list):
            return x
        
        elif x[0] == "if":
            if len(x) > 4:
                # elif statements
                i = 0
                while True:
                    if i == len(x):
                        break
                    item = x[i]
                    if item in ["if", "elif"]:
                        if eval(x[i + 1], ns):
                            exp = x[i + 2]
                            break
                        i += 3
                    elif item in ["else"]:
                        exp = x[i + 1]
                        break
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
                return None
            else:
                raise ErgonomicaError("[ergo: SyntaxError]: Wrong number of arguments for `set`. Should be: set symbol value.")
        
        elif x[0] == "global":
            (_, name, body) = x
            name = Symbol(name)
            namespace[name] = eval(body, ns)
            return None
        
        elif x[0] == "lambda":
            if len(x) > 2:
                argspec = x[1]
                body = x[2]
                return function(argspec, body, ns)
            else:
                raise ErgonomicaError("[ergo: SyntaxError]: Wrong number of arguments for `lambda`. Should be: lambda argspec body....")
        
            
        else:
            try:
                if isinstance(eval(x[0], ns), function):
                    p = eval(x[0], ns)
                    ns = Namespace(p.args, [eval(y, ns) for y in x[1:]], p.ns)
                    x = p.body
                    continue

                if arglist(eval(x[0], ns)) == ['argc']:
                    return eval(x[0], ns)(ArgumentsContainer(ENV, namespace, docopt(eval(x[0], ns).__doc__, [eval(i, ns) for i in x[1:]])))
                return eval(x[0], ns)(*[eval(i, ns) for i in x[1:]])
            except ErgonomicaError as e:
                if not e.args[0].startswith("[ergo]: NameError: No such variable {}.".format(x[0])):
                    # then it's not actually a unknown command---it's an error from something else
                    raise e
                # presumably the command isn't found
                ENV.update_env()
                try:
                    if isinstance(x[0], str) and x[0].startswith("%") or at_top:
                        PRINT_OVERRIDE = at_top
                        if x[0].startswith("%"):
                            x[0] = x[0][1:] # trim off percent sign
                        return os.system(" ".join([quote(y) for y in [x[0]] + expand_typed_args([eval(i, ns) for i in x[1:]])]))
                    else:
        
                        p = subprocess.Popen([x[0]] + expand_typed_args([eval(i, ns) for i in x[1:]]), stdout=subprocess.PIPE, universal_newlines=True)
                        try:
                            cur = [line[:-1] for line in iter(p.stdout.readline, "")]
                            if len(cur) == 1:
                                return cur[0]
                            else:
                                return cur
        
                        except KeyboardInterrupt as e:
                            p.terminate()
                            raise e
        
                except FileNotFoundError:
                    raise ErgonomicaError("[ergo]: Unknown command '{}'.".format(x[0]))
                
                except OSError: # on Python2
                    raise ErgonomicaError("[ergo]: Unknown command '{}'.".format(x[0]))
                

def main():
    """The main Ergonomica runtime."""

    args = sys.argv[1:]

    if (args != []) and (args[0] in ["--login", "-l"]):
        for line in file_lines(open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")).read()):
            print_ergo(line)
        args = args[1:]

    if args == []:
        # REPL loop
        while ENV.run:
            try:
                stdin = str(prompt(ENV, copy(namespace)))

                for line in file_lines(stdin):
                    print_ergo(line)


            # allow for interrupting functions. Ergonomica can still be
            # suspended from within Bash with C-z.
            except KeyboardInterrupt:
                print("[ergo: KeyboardInterrupt]: Exited.")
            
    elif ('--string' in args) or ('-s' in args):
        for string in args[1:]:
            print_ergo(string)
    

    elif args in [["--help"], ["-h"]]:
        print(__doc__)
    
    else:
        namespace['argv'] = args[1:]
        for line in file_lines(open(args[0]).read()):
           print_ergo(line)  


if __name__ == '__main__':
    main()
