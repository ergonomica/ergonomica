#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Ergonomica interpreter.

Usage:
  ergo.py [--login] [-r | --no-prompt-toolkit]
  ergo.py [--login] FILE [FILE_ARGV...]
  ergo.py [--login] [(-s | --string) STRING]

Options:
  --login         Source ~/.ergo/.ergo_profile on startup.
"""

import os
import sys
from copy import copy
from ergonomica.lib.lang.interpreter import namespace, ENV
from ergonomica.lib.lang.environment import Environment
from ergonomica.lib.interface.prompt import prompt
from ergonomica.lib.lang.interpreter import print_ergo, file_lines
from ergonomica.lib.lang.tokenizer import tokenize

try:
    input = raw_input
except NameError:
    pass

def main():
    """The main Ergonomica runtime."""

    args = sys.argv[1:]
    
    ENV.pipe_format_string = '[ergo: pipe]: (<operations_completed> operations completed) [<progress>] <percentage>%'

    if (args != []) and (args[0] in ["--login", "-l"]):
        for line in file_lines(open(os.path.join(os.path.expanduser("~"), ".ergo", ".ergo_profile")).read()):
            print_ergo(line)
        args = args[1:]
        
    use_ptk = True
    if ('-r' in args) or ('--no-prompttoolkit' in args):
        args = args[1:]
        use_ptk = False

    if args == []:
        # REPL loop
        while ENV.run:
            try:
                try:
                    if not use_ptk:
                        raise AssertionError
                    
                    stdin = str(prompt(ENV, copy(namespace)))                    
                            
                except AssertionError:
                    # we're not in a vt100 terminal (prompt_toolkit throws an AssertionError)
                    stdin = str(input(ENV.prompt))

                for line in file_lines(stdin):
                    print_ergo(line)

            # allow for interrupting functions. Ergonomica can still be
            # suspended from within Bash with C-z.
            except KeyboardInterrupt:
                print("[ergo: KeyboardInterrupt]: Exited.")
            except EOFError:
                break

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
