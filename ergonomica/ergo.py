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

import os
import uuid
import traceback
import sys
from copy import copy
import threading

# for escaping shell commands
try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote

from shlex import split

from ergonomica.lib.lang.docopt import docopt, DocoptException

#
# ergonomica library imports
#

from ergonomica.lib.interface.prompt import prompt
from ergonomica.lib.lib import ns
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.arguments import ArgumentsContainer

# initialize environment variables
ENV = Environment()
PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")

class Symbol(str):
    pass

class Function(object):
    def __init__(self, args, body, ns):
        self.args = args
        self.body = body
        self.ns = ns

    def __call__(self, *args):
        return eval(self.body[0], Namespace(self.args, args, self.ns))# for sexp in self.body]
    
class Namespace(dict):
    def __init__(self, argspec=(), args=(), outer=None):
        self.update(zip(argspec, args))
        self.outer = outer
    
    def find(self, var):
        return self if (var in self) else self.outer.find(var)


#def pipe(blocksizes, *lambdas):
    
    
def global_sum(*arguments):
    """
    Return the sum of all arguments, regardless of their type.
    """
    
    _sum = arguments[0]
    for i in arguments[1:]:
        _sum += i
    return _sum

def split_with_remainder(array, bs):
    new_arrays = [[]]
    for a in array:
        if len(new_arrays[-1]) < bs:
            new_arrays[-1].append(a)
        else:
            new_arrays.append([a])
    return new_arrays

def pipe(blocksizes, *functions):
    blocksizes = list(blocksizes)
    functions = list(functions)
    if len(functions) == 1:
        return functions[0]()
    else:
        bs = blocksizes.pop()
        f = functions.pop()
        # # if (stdin == []) and (not (bs == 0)):
        # #     raise Exception

        if bs == 0:
            return f(pipe(blocksizes, *functions))
        else:
            return [f(arr) for arr in split_with_remainder(pipe(blocksizes, *functions), bs)]
        
    
namespace = Namespace()
namespace.update({'print': lambda *x: x,
                  '+': global_sum,
                  '-': lambda a, b: a - b,
                  '^': lambda a, b: a ** b,
                  '/': lambda a, b: a / b,
                  '<=': lambda a, b: a <= b,
                  '*': lambda a, b: a * b,
                  '#t': True,
                  '#f': False,
                  '=': lambda *x: len(set(x)) == 1,
                  '!=': lambda *x: not (len(set(x)) == 1),
                  'type': lambda x: type(x).__name__,
                  'pipe': lambda blocksizes, *functions: pipe(blocksizes, *functions),
                  'first': lambda x: x[0],
                  'rest': lambda x: x[1:],
                  'list': lambda *x: list(x)})

for i in ns:
    namespace[i] = (lambda function: lambda *argv: function(ArgumentsContainer(ENV, namespace, docopt(function.__doc__, list(argv)))))(ns[i])

def ergo(stdin):
    """Wrapper for Ergonomica tokenizer and evaluator."""
    return eval(parse(tokenize(stdin)), namespace)

# def parse_sexp(sexp):
#     """Compile an Ergonomica s-expression down to pure ErgoLisp."""
#     parsed_sexp = []
#     is_piping = False
#     if "|" in sexp:
#         # then it's a piping expression
#         is_piping = True
#         parsed_sexp.append("pipe")
#         parsed_sexp.append()
#
#     for token in sexp:
#         if "|" in sexp:

def escape_parens(string):
    string_delim = False  # the wrapping quote
    escaped_string = [""]   # will be joined after completion
    for i in string:
        if i in ["(", ")"]:
            if not string_delim:
                escaped_string[-1] += "\x00" + i
                continue
            else:
                escaped_string[-1] += i
        elif i in ["\"", "'"]:
            escaped_string[-1] += i
            if string_delim:
                if string_delim == i:
                    string_delim = False
                    continue
            else:
                string_delim = i
                continue
        else:
            if (len(escaped_string) > 0):
                if (i == " ") and not string_delim:
                    escaped_string.append("")
                    pass
                else:
                    escaped_string[-1] += i
            else:
                escaped_string.append(i)

    return " ".join(escaped_string)

def tokenize(string):
    return pipe_compile(split(escape_parens(string).replace("\x00(", " ( ").replace("\x00)", " ) "), posix=False))

#def transpile_pipes(tokens):   
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
        
        if not parsed_command:
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

def pipe_compile(tokens):
    """
    Compile a list of ErgoLisp tokens that contain pipe characters to an expression using the `pipe` function.
    """
    
    if "|" in tokens:
        blocksizes = []
        expressions = [[]]
        for token in tokens:
            if token == "|":
                expressions.append([])
            else:
                expressions[-1].append(token)
        compiled_tokens = []
        for exp in expressions:
            compiled_tokens += ["(", "lambda", "(", "__stdin__", ")", "(", *convert_piping_tokens(exp)[1], ")", ")"]
            blocksizes.append(str(convert_piping_tokens(exp)[0]))
        return ["pipe", "(", "list"] + blocksizes + [")"] + compiled_tokens
    else: # nothing to be compiled
        return tokens

def convert_piping_tokens(_tokens):
    tokens = [x for x in _tokens]
    if "{}" in tokens:
        for i in range(len(tokens)):
            if tokens[i] == "{}":
                tokens[i] = "$__stdin__"
        return (0, tokens)

    blocksize = -1

    for i in range(len(tokens)):
        token = tokens[i]
        if isinstance(token, str) and token.startswith("{") and token.endswith("}"):
            content = token[1:-1] # the index code
            if "/" in content:
                blocksize = int(content.split("/")[1])
                tokens[i] = "$__stdin__[" + content.split("/")[0] + "]"
            else:
                if int(content) > blocksize:
                    blocksize = int(content)
                tokens[i] = "$__stdin__[" + content + "]"

    return (blocksize + 1, tokens)

def check_token(token):
    """Raise a SyntaxError on a malformed token."""
    if (token.startswith("'") and token.endswith("'")) or \
       (token.startswith("\"") and token.endswith("\"")):
        return
    
    
def atom(token, no_symbol=False):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            if token.startswith("'") or token.startswith("\""):
                return token[1:-1]
            elif no_symbol:
                return token
            else:
                return Symbol(token)

def eval(x, ns):
    if isinstance(x, Symbol):
        if ("[" in x) and ("]" in x):
            # TODO: handle invalid indices
            index = x[x.find("[") + 1:x.find("]")]
            return ns.find(x[:x.find("[")])[x[:x.find("[")]].__getitem__(atom(index, no_symbol=True))
        return ns.find(x)[x]
    elif isinstance(x, str):
        return x
    elif not isinstance(x, list):
        return x
    elif x[0] == "if":
        if len(x) == 4:
            (_, conditional, then, _else) = x
            exp = (then if eval(conditional, ns) else _else)
        else:
            (_, conditional, then) = x
            exp = (then if eval(conditional, ns) else None)
        return eval(exp, ns)
    elif x[0] == "define":
        (_, name, body) = x
        ns[name] = eval(body, ns)
    elif x[0] == "lambda":
        argspec = x[1]
        body = x[2:]
        return Function(argspec, body, ns)
    else:
        return eval(x[0], ns)(*[eval(i, ns) for i in x[1:]])


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
            stdout = eval_tokens(tokenize(open(arguments['FILE']).read() + "\n"), namespace,
                            log=log)

                # recursive_print(stdout)

        elif arguments['-m']:
            print(ergo(arguments['STRING'], log=log))

        else:

            # if run as login shell, run .ergo_profile
            if arguments['--login']:
                pass
                #print(ergo(open(PROFILE_PATH).read()))
                
                # recursive_print(stdout)

            # REPL loop
            while ENV.run:
                try:
                    stdin = str(prompt(ENV, copy(namespace)))
                    #stdin = raw_input("ergo>")
                    
                    stdout = ergo(stdin)
                    
                    if isinstance(stdout, list):
                        print("\n".join([str(x) for x in stdout]))
                    else:
                        print(stdout)
                    
                    # try:
                    #     # i.e., the process should be launched as a background thread
                    #     if stdin.startswith("(bg)"):
                    #         # build the computation tree (commands are only run when the tree is `recursive_print`ed)
                    #         stdout = eval_tokens(tokenize(stdin[4:] + "\n"), namespace, log=log)
                    #
                    #         # launch background thread
                    #         bg_thread = threading.Thread(target=recursive_print, args=[stdout])
                    #         bg_thread.start()
                    #
                    #     else:
                    #         stdout = eval_tokens(tokenize(stdin + "\n"), namespace, log=log)
                    #
                    #         # print/generator on the main thread
                    #         recursive_print(stdout)


                    # disable this because the traceback is printed
                    # pylint: disable=broad-except
                    # except Exception:
                    #     traceback.print_exc(file=sys.stdout)
                    #     continue


                # allow for interrupting functions. Ergonomica can still be
                # suspended from within Bash with C-z.
                except KeyboardInterrupt:
                    print("[ergo: KeyboardInterrupt]: Exited.")


if __name__ == '__main__':
    main()


    
