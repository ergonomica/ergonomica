#!/usr/bin/env python
# Copyright (C) 2020, Liam Schumm <contact@hexdump.email>.

"""
The main executable to launch Ergonomica.
"""

import os
import sys
from copy import copy
import click
from ergonomica.lib.lang.interpreter import namespace, ENV
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.interface.prompt import prompt
from ergonomica.lib.lang.interpreter import print_ergo, file_lines
from ergonomica.lib.lang.tokenizer import tokenize

@click.command()
@click.option('-f', '--file', required=False, type=click.Path(exists=True))
@click.argument('argv', nargs=-1, required=False)
def run(file, argv):
    """The main Ergonomica runtime."""

    for line in file_lines(open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")).read()):
        print_ergo(line)

    namespace['argv'] = argv
    if file:
        for line in file_lines(open(file).read()):
            print_ergo(line)
    else:
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
            except EOFError:
                break
