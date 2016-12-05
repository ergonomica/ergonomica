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
    parser.add_argument('-s', metavar='STRING', nargs='*', help="Run the specified strings in Ergonomica.")
    parser.add_argument('-f', metavar="FILE", type=str, help='Run the lines of FILE in Ergonomica.')
    parser.print_help()
    
def process_arguments(args):
    """Process arguments"""
    if args == []:
        return "shell"
    elif args[0] == "-f":
        return "run a file"
    elif args[0] == "--help":
        return "help"
    elif args[0] == "-s":
        return "run strings"
    return False
