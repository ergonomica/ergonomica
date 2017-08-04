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
from ergonomica.lib.lang.stdlib import Namespace, namespace

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
    
#def pipe(blocksizes, *lambdas):

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
    global namespace
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
    elif x[0] == "set":
        (_, name, body) = x
        ns[name] = eval(body, ns)
    elif x[0] == "global":
        (_, name, body) = x
        namespace[name] = eval(body, ns)
    elif x[0] == "lambda":
        argspec = x[1]
        body = x[2:]
        return Function(argspec, body, ns)
    else:
        try:
            return eval(x[0], ns)(*[eval(i, ns) for i in x[1:]])
        except AttributeError as e:
            print(e)
            # presumably the command isn't found
            try:
                p = subprocess.Popen([x[0]] + [eval(i, ns) for i in x[1:]], shell=True, stdout=subprocess.PIPE)
                out = []
                while p.poll() is None:
                    cur = str(p.stdout.readline())[2:-3]
                    out.append(cur)
                    print(cur)

                return cur
                
            except FileNotFoundError:
                return ("[ergo]: Unknown command '{}'.".format(x[0]))
            

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
                        if stdout != None:
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


    
