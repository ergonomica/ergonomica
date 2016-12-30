#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=W0703

# pylint messes up on readline for some reason
# pylint: disable=no-member

# pylint is silly with relative imports
# pylint: disable=relative-import

# decomposing comprehensions would be bad
# pylint: disable=line-too-long

# all code is client-side run under the user's account
# pylint: disable=eval-used

# pylint doesn't know where files are being imported
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=ungrouped-imports

# pylint: disable=wrong-import-position
# pylint: disable=invalid-name

# required for py2-3 cross compat
# pylint: disable=redefined-builtin

# this is why Python is used
# pylint: disable=redefined-variable-type

"""
[ergonomica.py]

The ergonomica runtime.
"""

from __future__ import print_function

try:
    input = raw_input
except NameError:
    pass

import os
import re
import sys

# lib/lib
_readline = True
try:
    from lib import readline
except ImportError:
    try:
        import readline
    except ImportError:
        _readline = False

# lib/lang
from lib.lang import completer
from lib.lang.parser import tokenize
from lib.lang.operator import get_operator, run_operator
from lib.lang.statement import get_statement
from lib.lang.arguments import get_args_kwargs, get_func
from lib.lang.environment import Environment
from lib.lang.error import ErgonomicaError, handle_runtime_error
from lib.lang.pipe import StaticPipeline
from lib.lang.stdout import handle_stdout
from lib.lang.bash import run_bash
from lib.lang.ergo2bash import ergo2bash

# lib/load
from lib.load.load_commands import verbs

# lib/misc
from lib.misc.arguments import print_arguments
from lib.misc.arguments import process_arguments

# set terminal title
sys.stdout.write("\x1b]2;ergonomica\x07")

# allow autocomplete (tab)
if _readline:
    readline.set_completer(completer.completer)
    readline.parse_and_bind("tab: complete")

# initialize environment
ENV = Environment()
ENV.verbs = verbs

if ENV.editor_mode:
    if _readline:
        readline.parse_and_bind('set editing-mode %s' % (ENV.editor_mode))

# read history
try:
    HIST_FILE = open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_history"), 'a')
    HIST = open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_history"), "r").read().split("\n")
    if _readline:
        for hist_item in HIST[:-1]:
            readline.add_history(hist_item)
except IOError as error:
    print("[ergo: ConfigError]: No such file ~/.ergo_history. Please run ergo_setup. " + str(error), file=sys.stderr)

# load .ergo_profile
verbs["load_config"](ENV, [], [])

debug = []

def ergo(stdin, depth=0):
    """Main ergonomica runtime."""

    global debug
    debug = []

    stdout = []

    ENV.ergo = ergo

    pipe = StaticPipeline()

    # macros
    for item in ENV.macros:
        stdin = stdin.replace(item, ENV.macros[item])

    num_blocks = len(stdin.split("->"))
    blocks = stdin.split("->")
    tokenized_blocks = [tokenize(block) for block in stdin.split("->")]

    debug.append("BLOCKS: " + str(blocks))
    debug.append("TOKENIZED_BLOCKS: " + str(tokenized_blocks))

    HIST_FILE.write(stdin + "\n")

    for i in range(0, len(blocks)):
        try:
            if i == 1:
                debug.append("1st iteration.")
            else:
                debug.append("%sth iteration." % (i))

            debug.append("Cleaning pipe...")

            # clean pipe
            pipe.prune()

            debug.append("Current pipe contents:")
            debug.append("pipe.args: " + str(pipe.args))
            debug.append("pipe.kwargs: " + str(pipe.kwargs))

            # update loop variables
            num_blocks -= 1

            # macros
            for item in ENV.macros:
                blocks[i] = blocks[i].replace(item, ENV.macros[item])

            # evaluate $(exp) & replace
            matches = re.findall(r"\$\((.*)\)", blocks[i])
            for match in matches:
                try:
                    blocks[i] = blocks[i].replace("$(%s)" % (match), " ".join(ergo(match)))
                except TypeError:
                    blocks[i] = blocks[i].replace("$(%s)" % (match), str(ergo(match)))

            # regenerate tokenized blocks
            tokenized_blocks[i] = tokenize(blocks[i])

            # more parse info
            statement = get_statement(blocks[i])
            evaluated_operator = run_operator(blocks[i], pipe)

            if blocks[i].strip() == "":
                debug.append("Empty command. Skipping.")

            elif evaluated_operator is not False:
                debug.append("Operator %s evaluated." % (get_operator(blocks[i])))
                stdout = evaluated_operator

            elif statement == "run":
                lines = [open(_file, "r").read().split("\n") for _file in tokenized_blocks[i][0][1:]]
                flattened_lines = [item for sublist in lines for item in sublist]
                stdout = map(ergo, flattened_lines)

            elif statement == "if":
                res = " ".join(tokenize(stdin.split(":", 1)[0])[0][1:])
                debug.append("STATEMENT-IF: conditional=%s command=%s" % (res.strip(), stdin.split(":", 1)[1].strip()))
                if ergo(res.strip()):
                    stdout = ergo(stdin.split(":", 1)[1].strip())
                else:
                    continue

            elif statement == "while":
                res = " ".join(tokenize(stdin.split(":", 1)[0])[0][1:])
                while ergo(res.strip()):
                    stdout = ergo(stdin.split(":", 1)[1].strip())
                else:
                    continue

            elif statement == "for":
                res = " ".join(tokenize(stdin.split(":")[0])[0][1:])
                stdout = []
                for item in ergo(res.strip()):
                    out = stdin.split(":", 1)[1]
                    out = out.replace(str(depth) + "{}", item)
                    stdout += ergo(out.strip(), depth+1)

            else:
                try:
                    func = get_func(tokenized_blocks[i], verbs)
                    args, kwargs = get_args_kwargs(tokenized_blocks[i], pipe)
                    stdout = func(ENV, args, kwargs)
                except Exception as error: #not in ergonomica path
                    try:
                        stdout = run_bash(ENV, ergo2bash(blocks[i]), pipe)
                    except:
                        stdout = str(error)


            # filter out none values
            try:
                if isinstance(stdout, list):
                    stdout = [x for x in stdout if x != None]
            except TypeError:
                stdout = []

        except Exception:
            _, error, _ = sys.exc_info()
            stdout = [handle_runtime_error(blocks[i], error)]

        handled_stdout = handle_stdout(stdout, pipe, num_blocks)
        if handled_stdout is not None:
            return handled_stdout

def print_ergo(stdin):
    """Print the result of ergo(stdin) properly."""
    try:
        stdout = ergo(stdin)
        if stdout is None:
            return
        try:
            if isinstance(stdout, list):
                for item in stdout:
                    # ANSI clear formatting char
                    print(item + ENV.default_color)
            else:
                print(stdout + ENV.default_color)
        except TypeError:
            print(stdout)
    except NameError:
        return
    except IndexError:
        return
    except Exception as error:
        print(error, file=sys.stderr)

GOAL = process_arguments(sys.argv)

if GOAL == "help":
    print_arguments()
    ENV.run = False

if GOAL == "run a file":
    LINES = open(sys.argv[2], "r").read().split("\n")
    map(print_ergo, LINES)

if GOAL == "run strings":
    map(print_ergo, sys.argv[2:])

if GOAL == "shell":
    while ENV.run:
        try:
            PROMPT = ENV.prompt
            PROMPT = PROMPT.replace(r"\u", ENV.user).replace(r"\w", ENV.directory)
            STDIN = input(PROMPT)
            print_ergo(STDIN)
        except KeyboardInterrupt:
            print("\n^C")

if GOAL == "devshell":
    while ENV.run:
        try:
            PROMPT = ENV.prompt
            PROMPT = PROMPT.replace(r"\u", ENV.user).replace(r"\w", ENV.directory)
            STDIN = input(PROMPT)
            print_ergo(STDIN)
            if len(sys.argv) > 2:
                open(sys.argv[2], "a").write("\n".join(debug))
            else:
                open("ergo.log", "a").write("\n".join(debug))
                #print("DEBUG:", "\n".join(debug))
        except KeyboardInterrupt:
            print("\n^C")
