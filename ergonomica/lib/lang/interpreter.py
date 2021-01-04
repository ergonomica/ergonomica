#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import inspect
import os
import uuid
import traceback
import sys
import threading
import subprocess
import types
import random
import time
import tempfile
from copy import copy
from threading import Thread
from math import floor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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

from ergonomica.lib.lib import ns
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.arguments import ArgumentsContainer
from ergonomica.lib.lang.builtins import Namespace, namespace
from ergonomica.lib.lang.parser import Symbol, parse, file_lines

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

def load(filename):
    for line in file_lines(open(filename).read()):
        stdout = ergo_to_string(line)
        if stdout:
            print(stdout)

namespace['load'] = load

def _tokenize(string):
    return tokenize(string)

namespace['.tokenize'] = _tokenize

def _parse(tokens):
    return parse(tokens)

namespace['.parse'] = _parse

def _eval(string):
    return ergo(string)

namespace['eval'] = _eval

def _eval_tokens(tokens):
    """
    Evaluate a tokenized Ergonomica expression in the namespace.
    
    Example:
        >>> _eval_tokens(['+', 2, ['-', 3, 9]])
        -4
    """
    global namespace
    return eval(tokens, namespace)

namespace['.eval_tokens'] = _eval_tokens

def _ast_to_string(tokens, depth = 0):
    if depth == 0:
        return " ".join([(_ast_to_string(x, depth + 1) if isinstance(x, list) else str(x)) for x in tokens])
    else:
        return "(" + " ".join([(_ast_to_string(x, depth + 1) if isinstance(x, list) else str(x)) for x in tokens]) + ")"
    
namespace['.ast_to_string'] = _ast_to_string

def _func_body(function):
    return function.body

namespace['.func_body'] = _func_body

def ergo(stdin, namespace=namespace):
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
    """
    Convert typed arguments (int, float, list) into a list of strings for parsing with Docopt.
    
    Example:
        >>> expand_typed_args([1, [2,3], 4, '5'])
        ['1', '2 3', '4', '5']
    """
    return [(" ".join([str(y) for y in x]) if isinstance(x, list) else str(x)) for x in args]

def stdout_to_string(stdout):
    """
    Convert the standard output of a function (STDOUT)
    """
    
    global PRINT_OVERRIDE
    
    if not PRINT_OVERRIDE:
        if isinstance(stdout, list):
            return "\n".join([str(x) for x in stdout if x != None])
        else:
            if stdout != None:
                return str(stdout)

    return ""

def ergo_to_string(stdin, namespace=namespace):
    """
    Wrapper for Ergonomica tokenizer and evaluator.
    """

    stdout = ergo(stdin, namespace)
    return stdout_to_string(stdout)

def print_ergo(stdin):
    global PRINT_OVERRIDE

    stdout = ergo_to_string(stdin)
    if stdout != "":
        print(stdout)
    PRINT_OVERRIDE = False

def spawn(function, *argv):
    pid = random.randint(0, 1024)
    Thread(target=lambda *argv: print("\n[ergo: spawn]: " + str(pid) + "\n" + stdout_to_string(function(*argv))), args=argv).start( )
    return pid

namespace['spawn'] = spawn

def edit_func(funcname):
    if not hasattr(namespace[funcname], 'body'):
        raise ErgonomicaError('[ergo: edit_func]: Function passed not a valid Ergonomica function! Perhaps it\'s a builtin?')
    # initialize tempfile and write current function body
    filename = tempfile.mktemp()
    open(filename, 'w').write(_ast_to_string(namespace[funcname].body))
    
    # start fsupdate thread
    threading.Thread(target = lambda: func_update(funcname, filename)).start()
    
    # return the tempfile name
    return filename    

def func_update(funcname, filename):
    """
    Allows one to rewrite a native SEXP function with your editor of choice.
    """

    global namespace

    class FsHandler(FileSystemEventHandler):
        def on_modified(self, event):
            namespace[funcname].body = _parse(_tokenize(open(filename, 'r').read().replace('\n', ' ')))
            
    event_handler = FsHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(filename), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

namespace['edit_func'] = edit_func
    
    

def _on_fs_update(path, function):
    """
    
    """

    class FsHandler(FileSystemEventHandler):
        def on_modified(self, event):
            print(stdout_to_string(function(event.src_path)))
            
    event_handler = FsHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def on_fs_update(path, function):
    """
    Whenever a filesystem change (entry creation/deletion) is detected at `path`, `function` is triggered with the name of the modified file or directory.
    """
    
    threading.Thread(target = lambda: _on_fs_update(path, function)).start()

namespace['on_fs_update'] = on_fs_update

def execfile(filename, *argv):
    """
    Execute an Ergonomica file at `filename` with arguments `argv` (stored in the argv variable).
    """
    
    mod_ns = copy(namespace)
    mod_ns['argv'] = argv
    for line in file_lines(open(filename).read()):
        stdout = ergo_to_string(line, mod_ns)
        if stdout:
            print(stdout)
    try:
        return mod_ns['main']()
    except KeyError:
        pass
    #return [ergo(line, mod_ns) for line in file_lines(open(filename).read())]

namespace['execfile'] = execfile


def split_with_remainder(array, bs):
    """
    Splits `array` into as many subsequences of length `bs` as possible---returning the remainder.
    
    Examples:
        >>> split_with_remainder([1,2,3,4,5,6,7], 3)
        [[1,2,3], [4,5,6], [7]]
    """
    
    new_arrays = [[]]
    for a in array:
        if len(new_arrays[-1]) < bs:
            new_arrays[-1].append(a)
        else:
            new_arrays.append([a])
    return new_arrays


def pipe(blocksizes, *functions):

    global ENV
    
    blocksizes = list(blocksizes)
    functions = list(functions)
    if len(functions) == 1:
        stdout = functions[0]([])

        # force output to be an array---if there's one output, make it
        # an array with one item
        if not isinstance(stdout, list):
            if type(stdout).__name__ == 'Flag':
                return [str(stdout)]
            else:
                return [stdout]
        else:
            return [str(x) if type(x).__name__ == 'Flag' else x for x in stdout]

    else:
        bs = blocksizes.pop()
        f = functions.pop()

        if bs == 0:
            return f(pipe(blocksizes, *functions))
        else:
            out = []
            stdin = split_with_remainder(pipe(blocksizes, *functions), bs)
            if stdin == [[]]:
                return []
            prev_percentage = 0
            prev_progress = 0
            max_bar_len = 0
            
            for i in range(len(stdin)):
                # here we use the floor function because you only want 100%
                percentage = int(floor(i * 100.0 / len(stdin)))
                progress = int(floor(prev_percentage / 100.0 * 15))
                
                if ENV.pipe_format_string:
                    if percentage != prev_percentage:
                        # then we need to re-write the bar
                        bar = ("[ergo: pipe]: " + ENV.pipe_format_string.replace('<operations_completed>', str(len(functions)))
                                                                                  .replace('<progress>', ENV.pipe_progress_char * int(floor(percentage / 100.0 * ENV.pipe_progress_length))
                                                                                                         + ' ' * (ENV.pipe_progress_length - int(floor(percentage / 100.0 * ENV.pipe_progress_length))))
                                                                                  .replace('<percentage>', str(percentage)) + '\r')
                        max_bar_len = len(bar) if len(bar) > max_bar_len else max_bar_len
                        sys.stdout.write(bar)
                        sys.stdout.flush()
                
                    prev_percentage = percentage
                    prev_progress = progress

                out.append(f(stdin[i]))
                
            if ENV.pipe_format_string:
                sys.stdout.write(' ' * max_bar_len + '\r')
                sys.stdout.flush()

            return out

namespace['pipe'] = pipe

if __name__ == "__main__":
    ENV.pipe_format_string = ""

def atom(token, no_symbol=False):
    try:
        return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            if token.startswith("'") or token.startswith("\""):
                return token[1:-1]
            elif no_symbol:
                return token
            else:
                return Symbol(token)

def arglist(_function):
    if isinstance(_function, function):
        return _function.args
    # they don't have args attributes since they're not actual Python functions
    if isinstance(_function, types.BuiltinFunctionType):
        return []
    elif isinstance(_function, types.FunctionType):
        return inspect.getargspec(_function).args
    else:
        try:
            return inspect.getargspec(function.__call__).args
        except AttributeError:
            raise ErgonomicaError("[ergo]: TypeError: '{}' is not a function.".format(str(function)))

namespace['arglist'] = arglist

# if arglist(eval(x[0], ns)) == ['argc']:
#     return eval(x[0], ns)(ArgumentsContainer(ENV, namespace, docopt(eval(x[0], ns).__doc__, [eval(i, ns) for i in x[1:]])))
# return eval(x[0], ns)(*[eval(i, ns) for i in x[1:]])
#

for f in namespace:
    if callable(namespace[f]):
        try:
            if arglist(namespace[f]) == ['argc']:
                old_func = copy(namespace[f])
                namespace[f] = (lambda func: lambda *argv: func(ArgumentsContainer(ENV, namespace, docopt(func.__doc__, argv))))(old_func)
        except TypeError:
            # is a builtin
            pass
        

def eval(x, ns, at_top = False):
    global namespace, PRINT_OVERRIDE, ENV
    print(x)

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
                raise ErgonomicaError("[ergo: SyntaxError]: Wrong number of arguments for `if`. Should be: `if conditional then_expr [elif conditional then_expr] [else]`.")
            return eval(exp, ns)

        elif x[0] == "set":
            if len(x) == 3:
                (_, name, body) = x
                name = Symbol(name)
                ns[name] = eval(body, ns)
                return None
            else:
                raise ErgonomicaError("[ergo: SyntaxError]: Wrong number of arguments for `set`. Should be: `set symbol value`.")

        elif x[0] == "with":
            # with (expr) as varname (body_expression)
            if len(x) == 5:
                (_, expr, _, varname, body_expression) = x
                name = Symbol(varname)
                copied_ns = copy(ns)
                copied_ns[name] = eval(expr, ns)
                return eval(body_expression, copied_ns)
            else:
                raise Ergonomica("[ergo: SyntaxError]: Wrong number of arguments for `with`. Should be: `with (expr) as varname (body_expression)`.")
            
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
                    ns = Namespace(p.args[::-1], [eval(y, ns) for y in x[1:]], p.ns)
                    x = p.body
                    continue

                # if arglist(eval(x[0], ns)) == ['argc']:
                #     return eval(x[0], ns)(ArgumentsContainer(ENV, namespace, docopt(eval(x[0], ns).__doc__, [eval(i, ns) for i in x[1:]])))
                return eval(x[0], ns)(*[eval(i, ns) for i in x[1:]])

            except Exception as e:
                if isinstance(e, ErgonomicaError):
                    if not e.args[0].startswith("[ergo]: NameError: No such variable {}.".format(x[0])):
                        # then it's not actually a unknown command---it's an error from something else
                        raise
                else:
                    print("[ergo]: Error on line:")
                    print(x)
                    raise
                        
                # presumably the command isn't found
                ENV.update_env()
                try:
                    if isinstance(x[0], str) and x[0].startswith("%") or at_top:
                        PRINT_OVERRIDE = at_top
                        if x[0].startswith("%"):
                            x[0] = x[0][1:] # trim off percent sign
                        os.symlink(os.path.expanduser("~"), "~")
                        try:
                            r = os.system(" ".join([quote(y) for y in [x[0]] + expand_typed_args([eval(i, ns) for i in x[1:]])]))
                            os.unlink("~")
                            return r
                        except Exception as e:
                            os.unlink("~")
                            raise e
                    else:
                        os.symlink(os.path.expanduser("~"), "~")
                        try:
                            p = subprocess.Popen([x[0]] + expand_typed_args([eval(i, ns) for i in x[1:]]), stdout=subprocess.PIPE, universal_newlines=True)
                            p.wait()
                            os.unlink("~")
                        except Exception as e:
                            os.unlink("~")
                            raise e
                        try:
                            cur = [line[:-1].encode().decode('utf-8') for line in iter(p.stdout.readline, "")]
                            if len(cur) == 1:
                                return cur[0]
                            else:
                                return cur

                        except KeyboardInterrupt as e:
                            p.terminate()
                            raise e

                except FileNotFoundError as e:
                    print(e)
                    raise ErgonomicaError("[ergo]: Unknown command '{}'.".format(x[0]))

                except OSError as e: # on Python2
                    print(e)
                    raise ErgonomicaError("[ergo]: Unknown command '{}'.".format(x[0]))


