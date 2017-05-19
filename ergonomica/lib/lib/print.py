#!/usr/bin/python
# -*- coding: utf-8 -*-

verbs = {}

def _print(argc):
    """
    print: Print strings.

    Usage:
       print <str>STRING... [-f INDICES] [-m MULTIPLIER]

    Options:
       -f INDICES : Print the items of the input with the specified indices.
       -c COUNT   : Print the given item COUNT times (seperated by newlines).  

    """
    
    return argc.args['STRING']

verbs["print"] = _print
