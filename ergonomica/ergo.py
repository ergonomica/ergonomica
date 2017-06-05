#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The Ergonomica interpreter.

Usage:
  ergo.py [--files FILE...] [--log] [--login]
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

from docopt import docopt

#
# ergonomica library imports
#

from ergonomica.lib.interface.prompt import prompt
from ergonomica.lib.lib import ns
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.lang.pipe import Pipeline, Operation
from ergonomica.lib.lang.tokenizer import tokenize
from ergonomica.lib.lang.parser_types import Function # , Command

# initialize environment variable
ENV = Environment()
PROFILE_PATH = os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")


def true(argc):
    """t: Return true.

    Usage:
       t
    """

    return [True]


def false(argc):
    """f: Return false.

    Usage:
       f
    """

    return [False]


ENV.ns.update(ns)
ENV.ns.update({"t": true,
               "f": false
              })


def ergo(stdin, log=False):
    """Wrapper for Ergonomica tokenizer and evaluator."""
    return eval_tokens(tokenize(stdin + "\n"), ENV.ns, log=log)


def eval_tokens(*args, **kwargs):
    """Wrapper to convert raw_eval_tokens (iterable) to a list."""
    return list(raw_eval_tokens(*args, **kwargs))

def raw_eval_tokens(_tokens, namespace, log=False, silent=False):
    """Evaluate Ergonomica tokens."""

    new_command = True
    in_function = False
    in_lambda = False
    argspec = False

    function = Function(eval_tokens)

    command_function = False
    args = []
    skip = False
    depth = 0
    lambda_depth = 0
    _lambda = []
    eval_next_expression = False
    current_indent = 0

    pipe = Pipeline(ENV, namespace)
    pipe.operations = []
    pipe.args = []

    tokens = _tokens

    tokens.append(tokenize("\n")[0])
    tokens[-1].type = 'EOF'

    for i in enumerate(tokens):

        token = i[1]

        if log:
            print("--- [ERGONOMICA LOG] ---")
            print("CURRENT TOKEN: ", token)
            print("CURRENT args : ", args)
            print("F is         : ", command_function)
            print("NEW_COMMAND  : ", new_command)
            print("IN_LAMBDA    : ", in_lambda)
            print("------------------------\n")

        if not in_function:
            if token.type == 'EVAL':
                eval_next_expression = True
                continue

            if token.type == 'LBRACKET':
                lambda_depth += 1
                in_lambda = True
                continue

            elif in_lambda:
                if token.type == 'RBRACKET':
                    lambda_depth -= 1

                if lambda_depth != 0:
                    _lambda.append(token)
                    continue

                else:  # time to wrap up the function
                    token.type = 'LITERAL'

                    if eval_next_expression:
                        token.value = eval_tokens(_lambda,
                                                  namespace,
                                                  log=log,
                                                  silent=silent)[0]
                        eval_next_expression = False
                    else:
                        lambda_uuid = str(uuid.uuid1())
                        partial = [_lambda, namespace, log, silent]
                        namespace[lambda_uuid] = lambda blank, s=partial: eval_tokens(s[0],
                                                                                      s[1],
                                                                                      s[2],
                                                                                      s[3])
                        token.value = lambda_uuid

                    _lambda = []
                    in_lambda = False

        if (token.type == 'EOF') or \
           ((token.type == 'NEWLINE') and (tokens[i[0] + 1].type != 'INDENT')):
            if in_function:
                in_function = False
                namespace.update(function.make())
            else:
                token.type = 'NEWLINE'

        # recognize commands as distinct from arguments
        if token.type == 'NEWLINE':

            argspec = False
            current_indent = 0
            skip = False

            if (len(tokens) > i[0] + 1) and tokens[i[0]+1].type == 'INDENT':
                function.append_to_body(token)
                continue

            if in_function:
                function.append_to_body(token)
                continue

            if command_function:
                pipe.append_operation(Operation(command_function, args))
                args = []
                command_function = False
                stdout = pipe.stdout()
                if (stdout != None) and (not silent):
                    yield stdout

                pipe = Pipeline(ENV, namespace)

            if skip:
                skip = False
                continue

            new_command = True
            continue

        if token.type == 'PIPE':
            try:
                pipe.append_operation(Operation(command_function, args))
            except KeyError:
                print("[ergo: CommandError]: Unknown command '%s'." % command_function)

            command_function = False
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
                function.append_to_body(token)
                continue

            elif not function.name:
                function.set_name(token.value)
                argspec = True
                continue

            elif argspec:
                function.argspec += " " + token.value
                continue

            function.append_to_body(token)
            continue

        if token.type == 'VARIABLE':
            token.type = 'LITERAL'
            token.value = str(namespace[token.value])

        if token.type == 'DEFINITION':
            in_function = True
            function = Function(eval_tokens)
            depth += 1
            continue

        elif (not new_command) and in_function:
            if not function.name:
                function.set_name(token.value)
            else:
                function.append_to_body(token)

        if new_command and in_function:
            function.append_to_body(token)

        elif new_command and (not in_function):
            if not command_function:
                try:
                    command_function = namespace[token.value]
                except KeyError:
                    if len(token.value) == 3:
                        possible_matches = [x for x in namespace if x.startswith(token.value)]
                        if len(possible_matches) == 1:
                            command_function = namespace[token.value]
                    #print("[ergo: CommandError]: Unknown command '%s'." % (token.value))
                    command_function = token.value

                new_command = False
                continue

        elif (not new_command) and (not in_function):
            args.append(token.value)

def main():
    """The main Ergonomica runtime."""

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

        elif arguments['-m']:
            print(ergo(arguments['STRING'], log=log))

        else:
            # persistent namespace across all REPL loops
            namespace = ENV.ns

            # if run as login shell, run .ergo_profile
            if arguments['--login']:
                eval_tokens(tokenize(open(PROFILE_PATH).read() + "\n"), ns, log=log, silent=True)

            # REPL loop
            while ENV.run:
                try:
                    stdin = prompt(ENV, namespace)
                    try:
                        stdout = eval_tokens(tokenize(stdin + "\n"), namespace, log=log)

                        if stdout is None:
                            pass
                        else:
                            for item in stdout:
                                if item != '':
                                    if isinstance(item, list):
                                        # map(print, list) doesn't work, so this is used
                                        [print(x) for x in item] # pylint: disable=expression-not-assigned
                                    else:
                                        print(stdout)

                    # disable this because the traceback is printed
                    # pylint: disable=broad-except
                    except Exception:
                        traceback.print_exc(file=sys.stdout)
                        continue


                # allow for interrupting functions. Ergonomica can still be
                # suspended from within Bash with C-z.
                except KeyboardInterrupt:
                    print("[ergo: KeyboardInterrupt]: Exited.")


if __name__ == '__main__':
    main()
