#!/usr/bin/python
# -*- coding: utf-8 -*-

verbs = {}

def _print(argc):
    """
    print: Print strings.

    Usage:
       print <str>STRING [-f INDICES...] [-m MULTIPLIER]

    Options:
       -f --filter     INDICES  Print the items of the input with the specified indices.
       -c --multiplier COUNT    Print the given item COUNT times (seperated by newlines).  

    """

    # strings = argc.args['STRING']
    # if argc.args['-f']:
        
    # filtered_strings = []
    
    
    
    return argc.args['STRING']

verbs["print"] = _print
