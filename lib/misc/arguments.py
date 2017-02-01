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
    parser.add_argument('-d', metavar="LOGFILE", type=str, help="Run Ergonomica in debug mode. If no LOGFILE specified, defaults to ergo.log")
    parser.print_help()
    
def process_arguments(args):
    """Process arguments"""
    if args[1:] == []:
        if args[0] != "test.py":
            return "shell"
    elif args[1:][0] == "-d":
        return "devshell"
    elif args[1:][0] == "-l":
        return "log"
    elif args[1:][0] == "-f":
        return "run a file"
    elif args[1:][0] == "--help":
        return "help"
    elif args[1:][0] == "-s":
        return "run strings"
    elif args[1:] != []:
        print("[ergo: ArgumentError] Use the -s argument to run strings.")
    return False
