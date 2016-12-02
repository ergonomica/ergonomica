#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/misc/arguments.py]

Handle command-line arguments for Ergonomica.
"""

import argparse

def print_arguments():
    """Print the ergonomica command line arguments."""
    parser = argparse.ArgumentParser(description='A Bash alternative written in Python.')
    parser.add_argument('--foo', type=int, default=42, help='FOO!')
    parser.print_help()
    
def process_arguments(args):
    """Process arguments"""
    if args == []:
        return "shell"
    elif args[0] == "-f":
        return "run a file"
    elif args[0] == "--help":
        return "help"
    return "run strings"
